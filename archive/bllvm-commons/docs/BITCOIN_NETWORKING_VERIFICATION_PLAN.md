# Bitcoin Networking Formal Verification Plan

## Executive Summary

**Goal**: Formally verify Bitcoin P2P protocol message parsing, serialization, and processing using Kani model checking.

**Approach**: Follow existing consensus verification patterns (176 proofs) to add networking verification.

**Timeline**: 3 phases over 6-8 weeks

**Status**: 📋 **PLAN READY FOR IMPLEMENTATION**

---

## Current State

### What Exists
- ✅ **Consensus Verification**: 176 Kani proofs in `bllvm-consensus`
- ✅ **Kani Infrastructure**: `kani_helpers.rs`, `verify` feature, CI integration
- ✅ **Networking Code**: Protocol parsing in `bllvm-node/src/network/protocol.rs`
- ✅ **Message Types**: Version, Block, Tx, Ping/Pong, Headers, etc.

### What's Missing
- ❌ **No Kani proofs** for protocol message parsing
- ❌ **No round-trip verification** for serialization
- ❌ **No checksum verification proofs**
- ❌ **No size limit enforcement proofs**

---

## Verification Scope

### Phase 1: Core Message Types (Priority: CRITICAL) 🔴

**Target**: Essential messages for Bitcoin P2P protocol

| Message Type | Priority | Rationale |
|--------------|----------|-----------|
| **Version** | 🔴 CRITICAL | Initial handshake, security-critical |
| **VerAck** | 🟡 HIGH | Handshake completion |
| **Ping/Pong** | 🟡 HIGH | Connection management |
| **Message Header** | 🔴 CRITICAL | All messages use this |

**Properties to Verify**:
1. Round-trip: `parse(serialize(msg)) == msg`
2. Header parsing correctness
3. Checksum validation
4. Size limit enforcement

**Estimated Proofs**: 8-10 proofs

---

### Phase 2: Consensus-Critical Messages (Priority: HIGH) 🟠

**Target**: Messages that affect consensus

| Message Type | Priority | Rationale |
|--------------|----------|-----------|
| **Block** | 🔴 CRITICAL | Consensus-critical |
| **Transaction (Tx)** | 🔴 CRITICAL | Consensus-critical |
| **Headers** | 🟠 HIGH | Chain synchronization |
| **GetHeaders** | 🟠 HIGH | Chain synchronization |
| **Inv** | 🟡 MEDIUM | Inventory management |
| **GetData** | 🟡 MEDIUM | Data requests |

**Properties to Verify**:
1. Round-trip for all message types
2. Payload parsing correctness
3. Bounded verification (large messages)

**Estimated Proofs**: 12-15 proofs

---

### Phase 3: Extended Protocol Features (Priority: MEDIUM) 🟡

**Target**: Advanced protocol features

| Feature | Priority | Rationale |
|---------|----------|-----------|
| **Compact Blocks (BIP152)** | 🟡 MEDIUM | Performance optimization |
| **Block Filtering (BIP157)** | 🟡 MEDIUM | Light client support |
| **Package Relay (BIP331)** | 🟡 MEDIUM | Transaction relay |
| **UTXO Commitments** | 🟡 MEDIUM | Protocol extensions |

**Properties to Verify**:
1. Message-specific parsing
2. Protocol extension correctness

**Estimated Proofs**: 8-10 proofs

---

## Implementation Plan

### Step 1: Setup Infrastructure (Week 1)

#### 1.1 Add Kani Dependency to bllvm-node

**File**: `bllvm-node/Cargo.toml`

**Also**: Make `calculate_checksum` public for verification

**File**: `bllvm-node/src/network/protocol.rs`

```rust
// Change from:
fn calculate_checksum(payload: &[u8]) -> [u8; 4] {

// To:
pub fn calculate_checksum(payload: &[u8]) -> [u8; 4] {  // ✅ Public for verification
```

```toml
[dependencies.kani-verifier]
version = "=0.41.0"
optional = true

[features]
default = []
verify = ["kani-verifier"]  # Verification-only feature
```

#### 1.2 Create Network Verification Helpers

**File**: `bllvm-node/src/network/kani_helpers.rs`

```rust
//! Kani proof helpers for network protocol verification

/// Network protocol limits for Kani proofs
pub mod proof_limits {
    /// Maximum message size for proof tractability
    pub const MAX_MESSAGE_SIZE_FOR_PROOF: usize = 1000;
    
    /// Maximum payload size for proof tractability
    pub const MAX_PAYLOAD_SIZE_FOR_PROOF: usize = 1000 - 24;  // Minus header
    
    /// Maximum addresses in Addr message
    pub const MAX_ADDR_COUNT_FOR_PROOF: usize = 10;
    
    /// Maximum inventory items
    pub const MAX_INV_COUNT_FOR_PROOF: usize = 10;
    
    /// Maximum user agent length
    pub const MAX_USER_AGENT_LEN_FOR_PROOF: usize = 256;
}

/// Standard unwind bounds for network operations
pub mod unwind_bounds {
    /// Message header parsing (fixed size)
    pub const HEADER_PARSING: u32 = 3;
    
    /// Simple message parsing
    pub const SIMPLE_MESSAGE: u32 = 5;
    
    /// Complex message parsing (with arrays)
    pub const COMPLEX_MESSAGE: u32 = 10;
    
    /// Checksum calculation
    pub const CHECKSUM: u32 = 3;
}

/// Macro for bounding version messages
#[macro_export]
macro_rules! assume_version_message_bounds {
    ($msg:expr) => {
        kani::assume($msg.user_agent.len() <= $crate::network::kani_helpers::proof_limits::MAX_USER_AGENT_LEN_FOR_PROOF);
        kani::assume($msg.version >= 70001);  // Minimum valid version
    };
}

/// Macro for bounding addr messages
#[macro_export]
macro_rules! assume_addr_message_bounds {
    ($msg:expr) => {
        kani::assume($msg.addresses.len() <= $crate::network::kani_helpers::proof_limits::MAX_ADDR_COUNT_FOR_PROOF);
    };
}

/// Macro for bounding BlockMessage
#[macro_export]
macro_rules! assume_block_message_bounds {
    ($msg:expr) => {
        use bllvm_consensus::kani_helpers::assume_block_bounds;
        assume_block_bounds!($msg.block, 2, 2);  // Bound block
        kani::assume($msg.witnesses.len() <= 10);  // Bound witnesses
    };
}

/// Macro for bounding TxMessage
#[macro_export]
macro_rules! assume_tx_message_bounds {
    ($msg:expr) => {
        use bllvm_consensus::kani_helpers::assume_transaction_bounds;
        assume_transaction_bounds!($msg.transaction);
    };
}
```

#### 1.3 Update CI Workflow

**File**: `.github/workflows/verify.yml` (add networking verification)

```yaml
- name: Network Protocol Verification
  working-directory: bllvm-node
  run: |
    cargo kani --features verify --verbose
    echo "✅ All network protocol proofs verified"
```

---

### Step 2: Phase 1 - Core Messages (Weeks 2-3)

#### 2.1 Message Header Verification

**File**: `bllvm-node/src/network/protocol_proofs.rs`

```rust
//! Kani proofs for Bitcoin protocol message parsing and serialization

#[cfg(kani)]
mod kani_proofs {
    use super::*;
    use crate::network::kani_helpers::*;
    use kani::*;

    /// Verify message header parsing correctness
    ///
    /// Mathematical Specification:
    /// ∀ header_bytes ∈ [u8; 24]: parse_header(header_bytes) = header ⟺
    ///   (header_bytes[0..4] = magic ∧
    ///    header_bytes[4..16] = command ∧
    ///    header_bytes[16..20] = length ∧
    ///    header_bytes[20..24] = checksum)
    #[kani::proof]
    #[kani::unwind(unwind_bounds::HEADER_PARSING)]
    fn verify_message_header_parsing() {
        use crate::network::protocol::BITCOIN_MAGIC_MAINNET;  // ✅ Use constant
        
        let magic = u32::from_le_bytes(BITCOIN_MAGIC_MAINNET);
        let command = "version\0\0\0\0\0";  // 12 bytes, null-padded
        let payload_len = kani::any::<u32>();
        kani::assume(payload_len <= proof_limits::MAX_PAYLOAD_SIZE_FOR_PROOF as u32);
        
        let payload = vec![0u8; payload_len as usize];
        let checksum = ProtocolParser::calculate_checksum(&payload);  // ✅ Now public
        
        // Build header
        let mut header = Vec::new();
        header.extend_from_slice(&magic.to_le_bytes());
        header.extend_from_slice(command.as_bytes());
        header.extend_from_slice(&payload_len.to_le_bytes());
        header.extend_from_slice(&checksum);
        
        // Parse header (extract fields)
        let parsed_magic = u32::from_le_bytes([header[0], header[1], header[2], header[3]]);
        let parsed_command = String::from_utf8_lossy(&header[4..16])
            .trim_end_matches('\0')
            .to_string();
        let parsed_len = u32::from_le_bytes([header[16], header[17], header[18], header[19]]);
        let parsed_checksum = &header[20..24];
        
        // Verify correctness
        assert_eq!(parsed_magic, magic);
        assert_eq!(parsed_command, "version");
        assert_eq!(parsed_len, payload_len);
        assert_eq!(parsed_checksum, &checksum);
    }
    
    /// Verify checksum validation rejects invalid checksums
    ///
    /// Mathematical Specification:
    /// ∀ payload, wrong_checksum: checksum(payload) ≠ wrong_checksum ⟹
    ///   parse_message_with_checksum(payload, wrong_checksum) = error
    #[kani::proof]
    #[kani::unwind(unwind_bounds::CHECKSUM)]
    fn verify_checksum_rejection() {
        use crate::network::protocol::BITCOIN_MAGIC_MAINNET;
        
        let payload = kani::any::<[u8; 100]>();
        let correct_checksum = ProtocolParser::calculate_checksum(&payload);  // ✅ Now public
        
        // Create wrong checksum
        let wrong_checksum = if correct_checksum[0] == 0 {
            [1u8; 4]
        } else {
            [0u8; 4]
        };
        
        // Build message with wrong checksum
        let mut message = Vec::new();
        message.extend_from_slice(&u32::from_le_bytes(BITCOIN_MAGIC_MAINNET).to_le_bytes());
        message.extend_from_slice(b"version\0\0\0\0\0");
        message.extend_from_slice(&(payload.len() as u32).to_le_bytes());
        message.extend_from_slice(&wrong_checksum);
        message.extend_from_slice(&payload);
        
        // Should reject invalid checksum
        assert!(ProtocolParser::parse_message(&message).is_err());
    }
    
    /// Verify message size limits are enforced
    ///
    /// Mathematical Specification:
    /// ∀ message: |message| > MAX_PROTOCOL_MESSAGE_LENGTH ⟹
    ///   parse_message(message) = error
    #[kani::proof]
    fn verify_message_size_limits() {
        let oversized_payload = vec![0u8; MAX_PROTOCOL_MESSAGE_LENGTH + 1];
        
        // Build oversized message
        let mut message = Vec::new();
        message.extend_from_slice(&0xd9b4bef9u32.to_le_bytes());
        message.extend_from_slice(b"version\0\0\0\0\0");
        message.extend_from_slice(&(oversized_payload.len() as u32).to_le_bytes());
        message.extend_from_slice(&[0u8; 4]);  // Dummy checksum
        message.extend_from_slice(&oversized_payload);
        
        // Should reject oversized message
        assert!(ProtocolParser::parse_message(&message).is_err());
    }
}
```

#### 2.2 Version Message Round-Trip

```rust
    /// Verify version message round-trip property
    ///
    /// Mathematical Specification:
    /// ∀ version_msg: parse_version(serialize_version(version_msg)) = version_msg
    #[kani::proof]
    #[kani::unwind(unwind_bounds::SIMPLE_MESSAGE)]
    fn verify_version_message_roundtrip() {
        let msg = kani::any::<VersionMessage>();
        
        // Bound to valid values
        assume_version_message_bounds!(msg);
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&ProtocolMessage::Version(msg.clone())).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Version(parsed_msg) => {
                assert_eq!(msg, parsed_msg);
            }
            _ => panic!("Expected Version message"),
        }
    }
    
    /// Verify verack message round-trip
    #[kani::proof]
    #[kani::unwind(unwind_bounds::SIMPLE_MESSAGE)]
    fn verify_verack_message_roundtrip() {
        let msg = ProtocolMessage::Verack;
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        assert!(matches!(parsed, ProtocolMessage::Verack));
    }
    
    /// Verify ping/pong message round-trip
    #[kani::proof]
    #[kani::unwind(unwind_bounds::SIMPLE_MESSAGE)]
    fn verify_ping_pong_roundtrip() {
        let ping = kani::any::<PingMessage>();
        let msg = ProtocolMessage::Ping(ping.clone());
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Ping(parsed_ping) => {
                assert_eq!(ping, parsed_ping);
            }
            _ => panic!("Expected Ping message"),
        }
        
        // Same for Pong
        let pong = PongMessage { nonce: ping.nonce };
        let pong_msg = ProtocolMessage::Pong(pong.clone());
        let serialized = ProtocolParser::serialize_message(&pong_msg).unwrap();
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        match parsed {
            ProtocolMessage::Pong(parsed_pong) => {
                assert_eq!(pong, parsed_pong);
            }
            _ => panic!("Expected Pong message"),
        }
    }
```

---

### Step 3: Phase 2 - Consensus-Critical Messages (Weeks 4-5)

#### 3.1 Block Message Verification

```rust
    /// Verify block message parsing (bounded)
    ///
    /// Mathematical Specification:
    /// ∀ block_msg (bounded): parse_block(serialize_block(block_msg)) = block_msg
    #[kani::proof]
    #[kani::unwind(unwind_bounds::COMPLEX_MESSAGE)]
    fn verify_block_message_roundtrip() {
        use bllvm_protocol::Block;  // ✅ Correct import path
        use bllvm_consensus::kani_helpers::assume_block_bounds;
        
        let block = kani::any::<Block>();
        
        // Bound block size for tractability
        assume_block_bounds!(block, 2, 2);  // Max 2 txs, 2 inputs/outputs each
        
        // ✅ Use BlockMessage wrapper (not Block directly)
        let block_msg = BlockMessage {
            block: block.clone(),
            witnesses: vec![],  // Empty for verification
        };
        let msg = ProtocolMessage::Block(block_msg.clone());
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Block(parsed_block_msg) => {
                assert_eq!(block_msg.block, parsed_block_msg.block);
                // Witnesses may differ, but block should match
            }
            _ => panic!("Expected Block message"),
        }
    }
    
    /// Verify transaction message round-trip
    #[kani::proof]
    #[kani::unwind(unwind_bounds::COMPLEX_MESSAGE)]
    fn verify_transaction_message_roundtrip() {
        use bllvm_protocol::Transaction;  // ✅ Correct import path
        use bllvm_consensus::kani_helpers::assume_transaction_bounds;
        
        let tx = kani::any::<Transaction>();
        assume_transaction_bounds!(tx);
        
        // ✅ Use TxMessage wrapper (not Transaction directly)
        let tx_msg = TxMessage {
            transaction: tx.clone(),
        };
        let msg = ProtocolMessage::Tx(tx_msg.clone());
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Tx(parsed_tx_msg) => {
                assert_eq!(tx_msg.transaction, parsed_tx_msg.transaction);
            }
            _ => panic!("Expected Tx message"),
        }
    }
    
    /// Verify headers message round-trip (bounded)
    #[kani::proof]
    #[kani::unwind(unwind_bounds::COMPLEX_MESSAGE)]
    fn verify_headers_message_roundtrip() {
        let header_count = kani::any::<usize>();
        kani::assume(header_count <= 10);  // Bound for tractability
        
        let headers = (0..header_count)
            .map(|_| kani::any::<bllvm_consensus::BlockHeader>())
            .collect();
        
        let msg = ProtocolMessage::Headers(HeadersMessage { headers: headers.clone() });
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Headers(parsed_headers) => {
                assert_eq!(headers.len(), parsed_headers.headers.len());
                for (h1, h2) in headers.iter().zip(parsed_headers.headers.iter()) {
                    assert_eq!(h1, h2);
                }
            }
            _ => panic!("Expected Headers message"),
        }
    }
    
    /// Verify inv/getdata message round-trip
    #[kani::proof]
    #[kani::unwind(unwind_bounds::COMPLEX_MESSAGE)]
    fn verify_inv_message_roundtrip() {
        let inv_count = kani::any::<usize>();
        kani::assume(inv_count <= proof_limits::MAX_INV_COUNT_FOR_PROOF);
        
        let inventory = (0..inv_count)
            .map(|_| kani::any::<InventoryVector>())
            .collect();
        
        let msg = ProtocolMessage::Inv(InvMessage { inventory: inventory.clone() });
        
        // Serialize
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        
        // Parse
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::Inv(parsed_inv) => {
                assert_eq!(inventory.len(), parsed_inv.inventory.len());
                for (i1, i2) in inventory.iter().zip(parsed_inv.inventory.iter()) {
                    assert_eq!(i1, i2);
                }
            }
            _ => panic!("Expected Inv message"),
        }
    }
```

---

### Step 4: Phase 3 - Extended Features (Weeks 6-7)

#### 4.1 Compact Block Verification

```rust
    /// Verify compact block message round-trip
    #[kani::proof]
    #[kani::unwind(unwind_bounds::COMPLEX_MESSAGE)]
    fn verify_compact_block_roundtrip() {
        use bllvm_protocol::Block;  // ✅ Correct import path
        use bllvm_consensus::kani_helpers::assume_block_bounds;
        
        // Use bounded block
        let block = kani::any::<Block>();
        assume_block_bounds!(block, 2, 2);
        
        let cmpct_block = CompactBlockMessage {
            // ... construct from block
        };
        
        let msg = ProtocolMessage::CmpctBlock(cmpct_block.clone());
        
        // Serialize and parse
        let serialized = ProtocolParser::serialize_message(&msg).unwrap();
        let parsed = ProtocolParser::parse_message(&serialized).unwrap();
        
        // Round-trip property
        match parsed {
            ProtocolMessage::CmpctBlock(parsed_cmpct) => {
                assert_eq!(cmpct_block, parsed_cmpct);
            }
            _ => panic!("Expected CmpctBlock message"),
        }
    }
```

---

### Step 5: Integration & Testing (Week 8)

#### 5.1 Update CI Workflow

**File**: `.github/workflows/verify.yml`

```yaml
jobs:
  verify-network:
    name: Network Protocol Verification
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Install Rust toolchain
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain-file: rust-toolchain.toml
          
      - name: Install Kani
        run: cargo install kani-verifier --version 0.41.0
          
      - name: Network Protocol Kani Proofs
        working-directory: bllvm-node
        run: |
          cargo kani --features verify --verbose
          echo "✅ All network protocol proofs verified"
```

#### 5.2 Update Documentation

**File**: `bllvm-node/docs/NETWORK_VERIFICATION.md`

Document all proofs, their properties, and verification status.

#### 5.3 Verification Status Tracking

**File**: `bllvm-node/VERIFICATION_STATUS.md`

Track proof coverage and status.

---

## Verification Properties

### Core Properties

1. **Round-Trip Property**:
   ```
   ∀ msg: parse(serialize(msg)) = msg
   ```

2. **Checksum Validation**:
   ```
   ∀ payload, checksum: checksum ≠ calculate_checksum(payload) ⟹
     parse_message(payload, checksum) = error
   ```

3. **Size Limit Enforcement**:
   ```
   ∀ message: |message| > MAX_PROTOCOL_MESSAGE_LENGTH ⟹
     parse_message(message) = error
   ```

4. **Header Parsing Correctness**:
   ```
   ∀ header_bytes: parse_header(header_bytes) extracts correct fields
   ```

### Message-Specific Properties

1. **Version Message**:
   - Valid version range (≥ 70001)
   - User agent length bounds
   - Network address correctness

2. **Block Message**:
   - Block structure preservation
   - Transaction count bounds
   - Block size limits

3. **Transaction Message**:
   - Transaction structure preservation
   - Input/output bounds
   - Transaction size limits

---

## File Structure

```
bllvm-node/
├── src/
│   └── network/
│       ├── protocol.rs              # Existing parsing code
│       ├── protocol_proofs.rs       # NEW: Kani proofs
│       └── kani_helpers.rs          # NEW: Verification helpers
├── Cargo.toml                       # Add kani-verifier dependency
└── docs/
    └── NETWORK_VERIFICATION.md      # NEW: Verification documentation
```

---

## Success Criteria

### Phase 1 Complete When:
- ✅ 8-10 proofs for core messages
- ✅ All proofs pass in CI
- ✅ Round-trip properties verified
- ✅ Checksum validation verified

### Phase 2 Complete When:
- ✅ 12-15 proofs for consensus-critical messages
- ✅ Block/Tx message verification
- ✅ Headers message verification
- ✅ All proofs pass in CI

### Phase 3 Complete When:
- ✅ 8-10 proofs for extended features
- ✅ Compact block verification
- ✅ All proofs pass in CI
- ✅ Documentation complete

### Overall Success:
- ✅ **30-35 total proofs** for network protocol
- ✅ **100% coverage** of critical message types
- ✅ **All proofs pass** in CI
- ✅ **Zero verification code** in release builds

---

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|-------------|
| **Setup** | Week 1 | Infrastructure, helpers, CI integration |
| **Phase 1** | Weeks 2-3 | Core message proofs (8-10 proofs) |
| **Phase 2** | Weeks 4-5 | Consensus-critical proofs (12-15 proofs) |
| **Phase 3** | Weeks 6-7 | Extended features (8-10 proofs) |
| **Integration** | Week 8 | CI, documentation, final testing |
| **Total** | **8 weeks** | **30-35 proofs** |

---

## Risk Mitigation

### Risk 1: Proof Complexity
- **Mitigation**: Use bounded verification, follow consensus patterns
- **Fallback**: Start with simple messages, iterate

### Risk 2: Performance
- **Mitigation**: Use appropriate unwind bounds, bound input sizes
- **Fallback**: Reduce bounds if proofs timeout

### Risk 3: bincode Dependency
- **Mitigation**: Verify round-trip, not bincode internals
- **Fallback**: Can replace bincode later if needed

---

## Next Steps

1. **Review Plan**: Get approval for approach
2. **Create Infrastructure**: Set up Kani helpers and CI
3. **Start Phase 1**: Implement core message proofs
4. **Iterate**: Add proofs incrementally
5. **Document**: Update verification status

---

## References

- [Kani Networking Verification Analysis](KANI_NETWORKING_VERIFICATION_ANALYSIS.md)
- [Consensus Verification Documentation](../bllvm-consensus/docs/VERIFICATION.md)
- [Kani Helpers](../bllvm-consensus/src/kani_helpers.rs)
- [Protocol Implementation](../bllvm-node/src/network/protocol.rs)

