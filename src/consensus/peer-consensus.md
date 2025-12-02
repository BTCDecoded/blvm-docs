# Peer Consensus Protocol

## Overview

Bitcoin Commons implements an N-of-M peer consensus protocol for UTXO set verification. The protocol discovers diverse peers and finds consensus among them to verify UTXO commitments without trusting any single peer.

## Architecture

### N-of-M Consensus Model

The protocol uses an N-of-M consensus model:

- **N**: Minimum number of peers required
- **M**: Target number of diverse peers
- **Threshold**: Consensus threshold (e.g., 70% agreement)
- **Diversity**: Peers must be diverse across ASNs, subnets, geographic regions

**Code**: ```1:6:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

### Peer Information

Peer information tracks diversity:

```rust
pub struct PeerInfo {
    pub address: IpAddr,
    pub asn: Option<u32>,               // Autonomous System Number
    pub country: Option<String>,        // Country code (ISO 3166-1 alpha-2)
    pub implementation: Option<String>, // Bitcoin implementation
    pub subnet: u32,                    // /16 subnet for diversity checks
}
```

**Code**: ```20:28:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Diverse Peer Discovery

### Diversity Requirements

Peers must be diverse across:

- **ASNs**: Maximum N peers per ASN
- **Subnets**: No peers from same /16 subnet
- **Geographic Regions**: Geographic diversity
- **Bitcoin Implementations**: Implementation diversity

**Code**: ```104:143:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

### Discovery Process

1. **Collect All Peers**: Gather all available peers
2. **Filter by ASN**: Limit peers per ASN
3. **Filter by Subnet**: Remove duplicate subnets
4. **Select Diverse Set**: Select diverse peer set
5. **Stop at Target**: Stop when target number reached

**Code**: ```111:143:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Consensus Finding

### Commitment Grouping

Commitments are grouped by their values:

- **Merkle Root**: UTXO commitment Merkle root
- **Total Supply**: Total Bitcoin supply
- **UTXO Count**: Number of UTXOs
- **Block Height**: Block height of commitment

**Code**: ```254:269:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

### Consensus Threshold

Consensus threshold check:

- **Threshold**: Configurable threshold (e.g., 70%)
- **Agreement Count**: Number of peers agreeing
- **Required Count**: `ceil(total_peers * threshold)`
- **Verification**: Check if agreement count >= required count

**Code**: ```294:333:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

### Mathematical Invariants

Consensus finding maintains invariants:

- `required_agreement_count <= total_peers`
- `required_agreement_count >= 1`
- `best_agreement_count <= total_peers`
- If `agreement_count >= required_agreement_count`, then `agreement_count/total_peers >= threshold`

**Code**: ```298:321:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Checkpoint Height Determination

### Median-Based Checkpoint

Checkpoint height determined from peer chain tips:

- **Median Calculation**: Uses median of peer tips
- **Safety Margin**: Subtracts safety margin to prevent deep reorgs
- **Mathematical Invariants**:
  - Median is always between min(tips) and max(tips)
  - Checkpoint height is always >= 0
  - Checkpoint height <= median_tip

**Code**: ```145:153:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Ban List Sharing

### Ban List Protocol

Nodes share ban lists to protect against malicious peers:

- **Ban List Messages**: `GetBanList`, `BanList` protocol messages
- **Hash Verification**: Ban list hash verification
- **Merging**: Ban list merging from multiple peers
- **Network-Wide Protection**: Protects entire network

**Code**: ```4310:4345:bllvm-node/src/network/mod.rs```

### Ban List Validation

Ban list entries are validated:

- **Entry Validation**: Each entry validated
- **Hash Verification**: Ban list hash verified
- **Merging Logic**: Merged with local ban list
- **Duplicate Prevention**: Duplicate entries prevented

**Code**: ```4316:4345:bllvm-node/src/network/mod.rs```

### Ban List Merging

Ban lists are merged from multiple peers:

- **Hash Verification**: Verify ban list hash
- **Entry Validation**: Validate each ban entry
- **Merging**: Merge with local ban list
- **Conflict Resolution**: Resolve conflicts (longest ban wins)

**Code**: ```1:24:bllvm-node/src/network/ban_list_merging.rs```

## Filtered Blocks

### Filtered Block Protocol

Nodes can request filtered blocks:

- **GetFilteredBlock**: Request filtered block
- **FilteredBlock**: Response with filtered block
- **Efficiency**: More efficient than full blocks
- **Privacy**: Better privacy for light clients

**Code**: ```56:59:bllvm-node/src/network/protocol.rs```

## Network-Wide Malicious Peer Protection

### Protection Mechanisms

Network-wide protection against malicious peers:

- **Ban List Sharing**: Share ban lists across network
- **Peer Reputation**: Track peer reputation
- **Auto-Ban**: Automatic banning of abusive peers
- **Eclipse Prevention**: Prevent eclipse attacks

**Code**: ```125:127:bllvm-node/SECURITY.md```

## Configuration

### Consensus Configuration

```rust
pub struct ConsensusConfig {
    pub min_peers: usize,              // Minimum peers required
    pub target_peers: usize,           // Target number of diverse peers
    pub consensus_threshold: f64,       // Consensus threshold (0.0-1.0)
    pub max_peers_per_asn: usize,     // Max peers per ASN
    pub safety_margin_blocks: Natural, // Safety margin for checkpoint
}
```

**Code**: ```56:93:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Benefits

1. **No Single Point of Trust**: No need to trust any single peer
2. **Diversity**: Diverse peer set reduces attack surface
3. **Consensus**: Majority agreement ensures correctness
4. **Network Protection**: Ban list sharing protects entire network
5. **Efficiency**: Filtered blocks reduce bandwidth

## Components

The peer consensus protocol includes:
- N-of-M consensus model
- Diverse peer discovery
- Consensus finding algorithm
- Checkpoint height determination
- Ban list sharing
- Filtered block protocol
- Network-wide malicious peer protection

**Location**: `bllvm-consensus/src/utxo_commitments/peer_consensus.rs`, `bllvm-node/src/network/ban_list_merging.rs`, `bllvm-node/src/network/mod.rs`

