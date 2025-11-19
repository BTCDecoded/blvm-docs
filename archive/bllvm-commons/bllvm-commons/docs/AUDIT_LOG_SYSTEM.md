# Audit Log System

## Overview

The BTCDecoded governance system implements a cryptographic audit logging system that creates a tamper-evident record of all governance operations. This provides complete transparency and accountability for all governance actions.

## Purpose

The audit log system serves as a **transparency and accountability mechanism** by:
- Recording all governance operations in tamper-evident format
- Creating immutable hash chain of all actions
- Enabling verification of governance integrity
- Providing complete audit trail for compliance

## Architecture

### Hash Chain Design

**Chain Structure**:
```
Genesis Entry: hash0 = SHA256(genesis_data)
Entry 1: hash1 = SHA256(entry1_data + hash0)
Entry 2: hash2 = SHA256(entry2_data + hash1)
Entry 3: hash3 = SHA256(entry3_data + hash2)
...
```

**Properties**:
- **Tamper Evidence**: Any modification breaks the chain
- **Ordering**: Entries are ordered by timestamp
- **Integrity**: Each entry verifies the previous entry
- **Immutability**: Cannot modify entries without detection

### Entry Format

**Audit Log Entry**:
```json
{
  "job_id": "pr_approval_1705320000_123",
  "job_type": "pr_approval",
  "timestamp": "2024-01-15T10:30:00Z",
  "server_id": "governance-01",
  "inputs_hash": "sha256:abc123...",
  "outputs_hash": "sha256:def456...",
  "previous_log_hash": "sha256:ghi789...",
  "this_log_hash": "sha256:jkl012...",
  "metadata": {
    "pr_number": 123,
    "maintainer_id": "maintainer_1",
    "signature": "ed25519_signature_hex",
    "status": "approved"
  }
}
```

**Field Descriptions**:
- **job_id**: Unique identifier for the operation
- **job_type**: Type of operation (pr_approval, maintainer_add, etc.)
- **timestamp**: When the operation occurred
- **server_id**: Which server performed the operation
- **inputs_hash**: Hash of operation inputs
- **outputs_hash**: Hash of operation outputs
- **previous_log_hash**: Hash of previous entry in chain
- **this_log_hash**: Hash of this entry
- **metadata**: Additional operation-specific data

## Storage Architecture

### File-Based Storage

**JSONL Format**:
```
{"job_id":"genesis_1705320000","job_type":"genesis",...}
{"job_id":"pr_approval_1705320001_123","job_type":"pr_approval",...}
{"job_id":"maintainer_add_1705320002_456","job_type":"maintainer_add",...}
```

**File Structure**:
```
/var/lib/governance/
├── audit-log.jsonl          # Current audit log
├── audit-log.2024-01.jsonl  # January 2024 log
├── audit-log.2024-02.jsonl  # February 2024 log
└── ...
```

**Benefits**:
- **Append-Only**: Natural append-only structure
- **Human Readable**: Easy to inspect and debug
- **Streaming**: Can process entries as they arrive
- **Backup Friendly**: Easy to backup and restore

### Database Storage (Optional)

**SQLite Integration**:
```sql
CREATE TABLE audit_log_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT UNIQUE NOT NULL,
    job_type TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    server_id TEXT NOT NULL,
    inputs_hash TEXT NOT NULL,
    outputs_hash TEXT NOT NULL,
    previous_log_hash TEXT NOT NULL,
    this_log_hash TEXT NOT NULL,
    metadata TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_job_id ON audit_log_entries(job_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log_entries(timestamp);
CREATE INDEX idx_audit_log_server_id ON audit_log_entries(server_id);
```

**Benefits**:
- **Query Performance**: Fast queries by various fields
- **Indexing**: Efficient lookups and filtering
- **Consistency**: ACID properties for data integrity
- **Integration**: Easy integration with other systems

## Hash Chain Implementation

### Entry Creation

**Canonical String Generation**:
```rust
impl AuditLogEntry {
    pub fn canonical_string(&self) -> String {
        format!(
            "{}{}{}{}{}{}{}{}",
            self.job_id,
            self.job_type,
            self.timestamp.to_rfc3339(),
            self.server_id,
            self.inputs_hash,
            self.outputs_hash,
            self.previous_log_hash,
            self.metadata.to_string()
        )
    }
    
    pub fn calculate_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.canonical_string().as_bytes());
        format!("sha256:{}", hex::encode(hasher.finalize()))
    }
}
```

**Hash Verification**:
```rust
impl AuditLogEntry {
    pub fn verify_hash(&self) -> bool {
        self.calculate_hash() == self.this_log_hash
    }
}
```

### Chain Verification

**Complete Chain Verification**:
```rust
use crate::audit::verify::verify_audit_log;

pub fn verify_audit_log(entries: &[AuditLogEntry]) -> Result<(), Error> {
    if entries.is_empty() {
        return Ok(());
    }
    
    // Check genesis entry
    if entries[0].previous_log_hash != GENESIS_HASH {
        return Err(Error::InvalidGenesis);
    }
    
    // Verify hash chain
    for i in 1..entries.len() {
        let current = &entries[i];
        let previous = &entries[i-1];
        
        // Verify previous hash reference
        if current.previous_log_hash != previous.this_log_hash {
            return Err(Error::BrokenChain);
        }
        
        // Verify entry hash
        if !current.verify_hash() {
            return Err(Error::InvalidHash);
        }
    }
    
    Ok(())
}
```

## Merkle Tree Construction

### Tree Building

**Merkle Node Structure**:
```rust
#[derive(Debug, Clone)]
pub struct MerkleNode {
    pub hash: String,
    pub left: Option<Box<MerkleNode>>,
    pub right: Option<Box<MerkleNode>>,
}

impl MerkleNode {
    pub fn new_leaf(hash: String) -> Self {
        Self {
            hash,
            left: None,
            right: None,
        }
    }
    
    pub fn new_parent(left: MerkleNode, right: MerkleNode) -> Self {
        let combined = format!("{}{}", left.hash, right.hash);
        let mut hasher = Sha256::new();
        hasher.update(combined.as_bytes());
        let hash = format!("sha256:{}", hex::encode(hasher.finalize()));
        
        Self {
            hash,
            left: Some(Box::new(left)),
            right: Some(Box::new(right)),
        }
    }
}
```

**Tree Construction**:
```rust
use crate::audit::merkle::build_merkle_tree;

pub fn build_merkle_tree(entries: &[AuditLogEntry]) -> Result<MerkleNode, Error> {
    if entries.is_empty() {
        return Err(Error::EmptyEntries);
    }
    
    let mut nodes: Vec<MerkleNode> = entries
        .iter()
        .map(|entry| MerkleNode::new_leaf(entry.this_log_hash.clone()))
        .collect();
    
    while nodes.len() > 1 {
        let mut next_level = Vec::new();
        let mut i = 0;
        
        while i < nodes.len() {
            if i + 1 < nodes.len() {
                let left = nodes.remove(i);
                let right = nodes.remove(i);
                next_level.push(MerkleNode::new_parent(left, right));
            } else {
                next_level.push(MerkleNode::single_child(nodes.remove(i)));
            }
        }
        
        nodes = next_level;
    }
    
    Ok(nodes.remove(0))
}
```

### Root Verification

**Merkle Root Verification**:
```rust
use crate::audit::merkle::verify_merkle_root;

pub fn verify_merkle_root(entries: &[AuditLogEntry], claimed_root: &str) -> Result<bool, Error> {
    if entries.is_empty() {
        return Ok(claimed_root == GENESIS_HASH);
    }
    
    let root = build_merkle_tree(entries)?;
    Ok(root.hash == claimed_root)
}
```

## Integration with Other Systems

### Nostr Integration

**Publish Audit Log Head**:
```rust
use crate::nostr::{NostrClient, StatusPublisher};

async fn publish_audit_log_head(client: &NostrClient, head_hash: &str, entry_count: u64) -> Result<(), Error> {
    let event = EventBuilder::new(
        Kind::Custom(30080),
        serde_json::json!({
            "head_hash": head_hash,
            "entry_count": entry_count,
            "timestamp": Utc::now()
        }).to_string(),
        vec![
            Tag::Generic(TagKind::Custom("d".into()), vec!["audit-head".to_string()]),
            Tag::Generic(TagKind::Custom("head_hash".into()), vec![head_hash.to_string()]),
        ],
    ).to_event(&client.keys)?;
    
    client.publish_event(event).await?;
    Ok(())
}
```

### OTS Integration

**Anchor Merkle Root**:
```rust
use crate::ots::anchor::RegistryAnchorer;

async fn anchor_audit_log_merkle_root(anchorer: &RegistryAnchorer, merkle_root: &str) -> Result<(), Error> {
    let merkle_data = serde_json::json!({
        "merkle_root": merkle_root,
        "timestamp": Utc::now(),
        "entry_count": entry_count
    });
    
    let proof = anchorer.ots_client.stamp(&serde_json::to_vec(&merkle_data)?).await?;
    
    // Store proof
    let proof_path = anchorer.proofs_path.join("audit-log-merkle.ots");
    std::fs::write(proof_path, proof)?;
    
    Ok(())
}
```

## Audit Log Rotation

### Rotation Strategy

**Time-Based Rotation**:
- **Frequency**: Monthly rotation
- **Trigger**: First day of each month
- **Action**: Create new log file, archive old one
- **Retention**: Keep 12 months of logs

**Size-Based Rotation**:
- **Threshold**: 100MB per log file
- **Action**: Create new log file when threshold reached
- **Naming**: Sequential numbering (audit-log.1.jsonl, audit-log.2.jsonl)

### Rotation Implementation

**Automatic Rotation**:
```rust
use crate::audit::logger::AuditLogger;

async fn rotate_audit_log(logger: &AuditLogger) -> Result<(), Error> {
    let now = Utc::now();
    let month_key = now.format("%Y-%m").to_string();
    
    // Create new log file
    let new_log_path = format!("/var/lib/governance/audit-log.{}.jsonl", month_key);
    let new_logger = AuditLogger::new(new_log_path)?;
    
    // Archive old log
    let old_log_path = logger.log_path.clone();
    let archive_path = format!("/var/lib/governance/archives/audit-log.{}.jsonl", month_key);
    std::fs::create_dir_all("/var/lib/governance/archives")?;
    std::fs::rename(&old_log_path, &archive_path)?;
    
    Ok(())
}
```

**Manual Rotation**:
```bash
# Rotate audit log manually
bllvm-commons audit rotate --log-path /var/lib/governance/audit-log.jsonl

# Archive old logs
bllvm-commons audit archive --log-path /var/lib/governance/audit-log.jsonl --archive-dir /var/lib/governance/archives/
```

## Verification and Validation

### CLI Verification Tools

**Verify Audit Log**:
```bash
# Verify complete audit log
bllvm-commons audit verify --log-path /var/lib/governance/audit-log.jsonl

# Verify specific entry
bllvm-commons audit verify-entry --log-path /var/lib/governance/audit-log.jsonl --entry-id "pr_approval_1705320000_123"

# Verify hash chain
bllvm-commons audit verify-chain --log-path /var/lib/governance/audit-log.jsonl
```

**Calculate Merkle Root**:
```bash
# Calculate Merkle root
bllvm-commons audit merkle-root --log-path /var/lib/governance/audit-log.jsonl

# Verify Merkle root
bllvm-commons audit verify-merkle --log-path /var/lib/governance/audit-log.jsonl --merkle-root "sha256:abc123..."
```

### Programmatic Verification

**Load and Verify**:
```rust
use crate::audit::{AuditLogger, verify_audit_log};

async fn verify_audit_log_file(log_path: &str) -> Result<(), Error> {
    let logger = AuditLogger::new(log_path.to_string())?;
    let entries = logger.load_all_entries().await?;
    
    // Verify hash chain
    verify_audit_log(&entries)?;
    
    // Calculate Merkle root
    let merkle_tree = build_merkle_tree(&entries)?;
    println!("Merkle root: {}", merkle_tree.hash);
    
    Ok(())
}
```

## Performance Considerations

### Storage Optimization

**Compression**:
```bash
# Compress old audit logs
gzip /var/lib/governance/archives/audit-log.2024-01.jsonl
gzip /var/lib/governance/archives/audit-log.2024-02.jsonl
```

**Indexing**:
```sql
-- Create indexes for common queries
CREATE INDEX idx_audit_log_job_type ON audit_log_entries(job_type);
CREATE INDEX idx_audit_log_server_id ON audit_log_entries(server_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log_entries(timestamp);
```

### Memory Management

**Streaming Processing**:
```rust
use std::io::{BufRead, BufReader};

async fn process_audit_log_streaming(log_path: &str) -> Result<(), Error> {
    let file = File::open(log_path)?;
    let reader = BufReader::new(file);
    
    let mut previous_hash = GENESIS_HASH.to_string();
    
    for line in reader.lines() {
        let line = line?;
        let entry: AuditLogEntry = serde_json::from_str(&line)?;
        
        // Verify hash chain
        if entry.previous_log_hash != previous_hash {
            return Err(Error::BrokenChain);
        }
        
        if !entry.verify_hash() {
            return Err(Error::InvalidHash);
        }
        
        previous_hash = entry.this_log_hash;
    }
    
    Ok(())
}
```

## Security Considerations

### Tamper Detection

**Hash Chain Integrity**:
- Any modification to an entry breaks the chain
- Impossible to modify entries without detection
- Chain verification detects any tampering

**Entry Validation**:
- All entries must have valid signatures
- Timestamps must be monotonic
- Server IDs must be authorized

### Access Control

**File Permissions**:
```bash
# Set restrictive permissions
chmod 600 /var/lib/governance/audit-log.jsonl
chown governance:governance /var/lib/governance/audit-log.jsonl
```

**Backup Security**:
```bash
# Encrypt backups
gpg --symmetric --cipher-algo AES256 /var/lib/governance/audit-log.jsonl
```

## Monitoring and Alerting

### Health Monitoring

**Log Health Checks**:
```bash
# Check audit log health
bllvm-commons audit health --log-path /var/lib/governance/audit-log.jsonl

# Monitor log growth
watch -n 60 'wc -l /var/lib/governance/audit-log.jsonl'
```

**Automated Monitoring**:
```rust
use crate::audit::AuditLogger;

async fn monitor_audit_log_health(logger: &AuditLogger) -> Result<(), Error> {
    // Check log file size
    let metadata = std::fs::metadata(&logger.log_path)?;
    if metadata.len() > 100 * 1024 * 1024 { // 100MB
        println!("Warning: Audit log size exceeded 100MB");
    }
    
    // Check entry count
    let entry_count = logger.get_entry_count().await;
    if entry_count > 100000 {
        println!("Warning: Audit log entry count exceeded 100,000");
    }
    
    // Check last entry timestamp
    let head_hash = logger.get_head_hash().await;
    if head_hash.is_empty() {
        println!("Warning: Audit log is empty");
    }
    
    Ok(())
}
```

## Troubleshooting

### Common Issues

1. **Hash Chain Broken**
   - Check for corrupted entries
   - Verify file integrity
   - Restore from backup if necessary

2. **Entry Verification Failed**
   - Check entry format
   - Verify hash calculation
   - Check for data corruption

3. **Merkle Root Mismatch**
   - Recalculate Merkle root
   - Check for missing entries
   - Verify entry order

### Debug Commands

```bash
# Debug audit log
bllvm-commons audit debug --log-path /var/lib/governance/audit-log.jsonl

# Check specific entry
bllvm-commons audit inspect --log-path /var/lib/governance/audit-log.jsonl --entry-id "pr_approval_1705320000_123"

# Validate log format
bllvm-commons audit validate --log-path /var/lib/governance/audit-log.jsonl
```

## References

- [Verification Guide](VERIFICATION.md)
- [Nostr Integration](NOSTR_INTEGRATION.md)
- [OTS Integration](OTS_INTEGRATION.md)
- [Configuration Reference](CONFIGURATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
