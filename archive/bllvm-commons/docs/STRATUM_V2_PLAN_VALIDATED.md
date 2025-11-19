# Stratum V2 Integration Plan - Validated and Adjusted

## Validation Summary

**Plan Status**: ✅ Validated against architecture
**Adjustments Made**: Enhanced with technical details, clarified integration points, specified TLV encoding

## Overview

Add Stratum V2 protocol support to the bllvm-node for mining operations, leveraging the existing transport abstraction layer to support both TCP and Iroh/QUIC transports. This enables encrypted mining pool communication, efficient binary protocol (50-66% bandwidth savings), and eventually merge mining coordination via multiplexed channels.

## Architecture Validation

```
MiningCoordinator (bllvm-node/src/node/miner.rs)
    ├──► MiningEngine (existing - local mining)
    ├──► MiningRpc (existing - JSON-RPC mining)  
    └──► StratumV2Client (NEW - pool mining)
            ↓ (uses NetworkManager)
        NetworkManager (bllvm-node/src/network/mod.rs)
            ↓ (transport abstraction - proven with UTXO commitments)
        Transport Trait (bllvm-node/src/network/transport.rs)
            ├──► TcpTransport ──► Stratum V2 over TCP
            └──► IrohTransport ──► Stratum V2 over QUIC (encrypted, multiplexed)
```

**Validation**:
- ✅ Transport abstraction pattern proven with UTXO commitments
- ✅ NetworkManager integration pattern established
- ✅ MiningCoordinator structure supports extension
- ✅ Configuration system (NodeConfig) ready for extension

## Implementation Phases

### Phase 1: Stratum V2 Miner Client (Standard Mining)

**Goal**: Enable bllvm-node to connect to Stratum V2 mining pools as a miner.

**Components to Implement**:

1. **Stratum V2 Protocol Module** (`bllvm-node/src/network/stratum_v2/`)
   
   **Files to Create**:
   - `mod.rs`: Module interface with `#[cfg(feature = "stratum-v2")]`
   - `protocol.rs`: TLV encoder/decoder, protocol framing
   - `messages.rs`: All Stratum V2 message types
   - `error.rs`: Stratum V2-specific error types
   - `client.rs`: `StratumV2Client` struct (transport-agnostic)
   - `miner.rs`: Miner role implementation

   **Protocol Details**:
   - **TLV Encoding**: Tag (u16), Length (u32), Value (Vec<u8>)
   - **Message Types**: SetupConnection, OpenMiningChannel, NewMiningJob, SetNewPrevHash, SubmitShares, SubmitSharesSuccess, SubmitSharesError
   - **Framing**: Length-prefixed messages (4-byte length prefix before TLV data)

2. **Protocol Adapter Pattern**
   
   Follow the `protocol_adapter.rs` pattern:
   - Serialize Stratum V2 messages to wire format
   - TCP: Standard Stratum V2 binary format (TLV with length prefix)
   - Iroh: Same binary format (QUIC handles stream framing)
   - Deserialize incoming messages

3. **Integration with MiningCoordinator**
   
   **Modify** `bllvm-node/src/node/miner.rs`:
   ```rust
   pub struct MiningCoordinator {
       mining_engine: MiningEngine,
       transaction_selector: TransactionSelector,
       mempool_provider: MockMempoolProvider,
       #[cfg(feature = "stratum-v2")]
       stratum_v2_client: Option<StratumV2Client>, // NEW
   }
   ```
   
   **Add trait** (similar to `MempoolProvider`):
   ```rust
   #[cfg(feature = "stratum-v2")]
   pub trait StratumV2TemplateProvider: Send + Sync {
       async fn get_current_job(&self) -> Result<Block>;
       async fn submit_share(&self, share: ShareData) -> Result<ShareResult>;
   }
   ```

4. **NetworkManager Integration**
   
   **Modify** `bllvm-node/src/network/mod.rs`:
   - Add `#[cfg(feature = "stratum-v2")] pub mod stratum_v2;`
   - Add Stratum V2 message types to `NetworkMessage` enum:
     ```rust
     #[cfg(feature = "stratum-v2")]
     StratumV2MessageReceived(Vec<u8>, SocketAddr), // (data, peer_addr)
     ```
   - Add message handler in `process_messages()` method

5. **Configuration**
   
   **Modify** `bllvm-node/src/config/mod.rs`:
   ```rust
   pub struct NodeConfig {
       // ... existing fields ...
       #[cfg(feature = "stratum-v2")]
       pub stratum_v2: Option<StratumV2Config>,
   }
   
   #[cfg(feature = "stratum-v2")]
   pub struct StratumV2Config {
       pub enabled: bool,
       pub pool_url: Option<String>, // Format: "tcp://pool:3333" or "iroh://<nodeid>"
       pub listen_addr: Option<SocketAddr>, // For server mode
       pub transport_preference: TransportPreferenceConfig,
       pub merge_mining_enabled: bool,
   }
   ```

**Files to Create**:
- `bllvm-node/src/network/stratum_v2/mod.rs`
- `bllvm-node/src/network/stratum_v2/protocol.rs`
- `bllvm-node/src/network/stratum_v2/messages.rs`
- `bllvm-node/src/network/stratum_v2/error.rs`
- `bllvm-node/src/network/stratum_v2/client.rs`
- `bllvm-node/src/network/stratum_v2/miner.rs`

**Files to Modify**:
- `bllvm-node/src/network/mod.rs` - Add module and message types
- `bllvm-node/src/node/miner.rs` - Integrate StratumV2Client
- `bllvm-node/src/config/mod.rs` - Add StratumV2Config
- `bllvm-node/Cargo.toml` - Add `stratum-v2` feature flag

**Key Features**:
- Setup Connection handshake (protocol version negotiation)
- Open Mining Channel (job negotiation - miner controls transaction selection)
- Template distribution (NewMiningJob, SetNewPrevHash)
- Share submission (SubmitShares with local validation)
- Error handling and automatic reconnection
- Works with TCP and Iroh transports automatically (via transport abstraction)

### Phase 2: Stratum V2 Mining Pool Server

**Goal**: Enable bllvm-node to act as a Stratum V2 mining pool server.

**Components to Implement**:

1. **Server Module** (`bllvm-node/src/network/stratum_v2/`)
   - `server.rs`: `StratumV2Server` struct (listens for miner connections)
   - `pool.rs`: Pool role implementation
     - Template generation from `MiningCoordinator`
     - Share validation using `bllvm-consensus::pow::check_proof_of_work()`
     - Difficulty management
     - Miner connection management

2. **Integration**:
   - Add `stratum_v2_server: Option<StratumV2Server>` to `NetworkManager`
   - Server listens via transport abstraction (TCP and/or Iroh)
   - Uses `MiningCoordinator::generate_block_template()` for templates
   - Validates shares using bllvm-consensus functions

**Files to Create**:
- `bllvm-node/src/network/stratum_v2/server.rs`
- `bllvm-node/src/network/stratum_v2/pool.rs`

**Files to Modify**:
- `bllvm-node/src/network/mod.rs` - Add server to NetworkManager
- `bllvm-node/src/config/mod.rs` - Add server configuration

### Phase 3: Merge Mining Coordination

**Goal**: Support merge mining via Stratum V2 multiplexed channels.

**Components to Implement**:

1. **Merge Mining Module** (`bllvm-node/src/network/stratum_v2/`)
   - `merge_mining.rs`: Merge mining coordination logic
     - Multi-chain channel management
     - Template coordination (Bitcoin + secondary chains)
     - Reward tracking across chains
     - Revenue distribution calculation (1% fee per whitepaper: 60% core, 25% grants, 10% audits, 5% ops)

2. **Protocol Extensions**:
   - Extend `OpenMiningChannel` to support multiple chains
   - Add merge mining message types
   - Channel ID mapping (one channel per chain, multiplexed over single connection)

**Files to Create**:
- `bllvm-node/src/network/stratum_v2/merge_mining.rs`

**Files to Modify**:
- `bllvm-node/src/network/stratum_v2/messages.rs` - Add merge mining message types
- `bllvm-node/src/network/stratum_v2/client.rs` - Add merge mining support
- `bllvm-node/src/network/stratum_v2/server.rs` - Add merge mining support

## Technical Details

### Transport Abstraction Pattern (Validated)

**Proven Pattern** (from UTXO commitments):
- `StratumV2Client` struct holds `Arc<RwLock<NetworkManager>>`
- Uses `NetworkManager::send_to_peer()` for sending
- Uses `NetworkManager::process_messages()` for receiving
- Automatic transport selection based on `TransportAddr`
- Protocol adapter handles message serialization

**Example Structure** (similar to `UtxoCommitmentsClient`):
```rust
#[cfg(feature = "stratum-v2")]
pub struct StratumV2Client {
    network_manager: Arc<RwLock<NetworkManager>>,
    pool_url: String,
    // ... other state
}

impl StratumV2Client {
    pub async fn connect(&self) -> Result<()> {
        // Parse pool_url to get TransportAddr
        // Use NetworkManager to connect
        // Initialize Stratum V2 session
    }
    
    pub async fn get_current_job(&self) -> Result<Block> {
        // Request current job from pool
        // Convert Stratum V2 template to Block
    }
}
```

### Protocol Specifications

**Stratum V2 Binary Protocol**:
- **Encoding**: Tag-Length-Value (TLV)
  - Tag: u16 (message type)
  - Length: u32 (payload size in bytes)
  - Value: Vec<u8> (message payload)
- **Framing**: Length-prefixed (4-byte length before TLV)
- **Specification**: https://stratumprotocol.org/
- **Message Types**: All from Stratum V2 specification
- **Efficiency**: 50-66% bandwidth savings vs Stratum V1

**Encryption**:
- TCP: Stratum V2's built-in AEAD encryption
- Iroh: QUIC/TLS encryption (additional layer, compatible)
- Both provide end-to-end encryption

**Multiplexing** (for merge mining):
- QUIC natively supports stream multiplexing
- Each mining channel uses separate QUIC stream
- One connection can handle multiple chains

### Dependencies

**No external Stratum V2 library needed**:
- Implement from Stratum V2 specification
- Use existing dependencies:
  - `tokio` (already in Cargo.toml)
  - `async-trait` (already in Cargo.toml)
  - `serde` (for configuration, not protocol - protocol is binary TLV)
  - Transport infrastructure (already implemented)

**Cargo.toml Changes**:
```toml
[features]
stratum-v2 = []  # No additional dependencies needed
```

### Integration Points (Validated)

**With MiningCoordinator**:
- Location: `bllvm-node/src/node/miner.rs`
- Current structure: Has `MiningEngine`, `TransactionSelector`, `MempoolProvider`
- Integration: Add optional `StratumV2Client` field
- Template source selection: Use pool template when Stratum V2 enabled, local otherwise

**With NetworkManager**:
- Location: `bllvm-node/src/network/mod.rs`
- Pattern: Similar to UTXO commitments message routing
- Add Stratum V2 message handler to `process_messages()`
- Use `send_to_peer()` for sending messages

**With Configuration**:
- Location: `bllvm-node/src/config/mod.rs`
- Extend `NodeConfig` with `StratumV2Config`
- JSON serialization/deserialization support
- Runtime configuration loading

## Testing Strategy

1. **Unit Tests** (`bllvm-node/tests/stratum_v2/`)
   - TLV encoder/decoder correctness
   - Message type serialization/deserialization
   - Error handling

2. **Integration Tests**:
   - Miner client → test pool (TCP)
   - Miner client → test pool (Iroh)
   - Server accepting miners (TCP and Iroh)
   - Template distribution and share submission

3. **Transport Tests**:
   - Verify TCP transport works
   - Verify Iroh transport works (should work automatically)
   - Verify hybrid mode (some TCP, some Iroh miners)

4. **Merge Mining Tests** (Phase 3):
   - Multi-chain template coordination
   - Channel multiplexing over single connection
   - Revenue tracking accuracy

## Success Criteria

**Phase 1 (Miner Client)**:
- ✅ Miner connects to Stratum V2 pool via TCP
- ✅ Miner connects to Stratum V2 pool via Iroh (automatic via transport abstraction)
- ✅ Job negotiation works (Open Mining Channel)
- ✅ Template reception and processing works
- ✅ Share submission works (with local validation)
- ✅ Integration with MiningCoordinator functional
- ✅ Backward compatibility maintained (local mining still works)

**Phase 2 (Pool Server)**:
- ✅ Server accepts miner connections (TCP and Iroh)
- ✅ Template generation from MiningCoordinator
- ✅ Template distribution to miners
- ✅ Share validation using bllvm-consensus
- ✅ Share acceptance/rejection
- ✅ Multi-miner support

**Phase 3 (Merge Mining)**:
- ✅ Multiple mining channels per connection
- ✅ Multi-chain template coordination
- ✅ Simultaneous share submission for all chains
- ✅ Reward tracking per chain
- ✅ Revenue distribution calculation (1% fee structure)

## Implementation Order (Validated)

1. **Protocol Foundation**:
   - TLV encoder/decoder (`protocol.rs`)
   - Message type definitions (`messages.rs`)
   - Error types (`error.rs`)

2. **Client Infrastructure**:
   - Transport-agnostic client struct (`client.rs`)
   - Protocol adapter for message serialization
   - Integration with NetworkManager

3. **Miner Role**:
   - Miner implementation (`miner.rs`)
   - Setup Connection, Open Mining Channel
   - Template handling (convert Stratum V2 format to Block)
   - Share submission

4. **Transport Testing**:
   - Test TCP transport
   - Test Iroh transport (verify automatic support)
   - Test hybrid mode

5. **MiningCoordinator Integration**:
   - Add Stratum V2 client to MiningCoordinator
   - Template source selection logic
   - Maintain backward compatibility

6. **Server Role** (Phase 2):
   - Server implementation (`server.rs`)
   - Pool role (`pool.rs`)
   - Integration with NetworkManager

7. **Merge Mining** (Phase 3):
   - Merge mining module (`merge_mining.rs`)
   - Protocol extensions
   - Revenue tracking

## Adjustments Made

1. **Clarified TLV Encoding**: Specified Tag (u16), Length (u32), Value (Vec<u8>) format
2. **Enhanced Integration Details**: Provided code snippets showing exact integration points
3. **Validated Transport Pattern**: Confirmed transport abstraction works automatically for Iroh
4. **Specified File Locations**: Exact paths for all files to create/modify
5. **Added Protocol Details**: Message framing, encryption details, multiplexing approach
6. **Configuration Structure**: Detailed configuration struct design
7. **Dependency Clarification**: Confirmed no external library needed (implement from spec)

## Notes

- **Follow UTXO Commitments Pattern**: Proven transport abstraction approach
- **No Library Dependency**: Implement from Stratum V2 specification (no mature Rust library exists)
- **Backward Compatibility**: Stratum V2 is optional - existing mining still works
- **Transport Abstraction**: Iroh support is automatic via transport layer (like UTXO commitments)
- **Binary Protocol**: 50-66% bandwidth savings vs Stratum V1 (per whitepaper)
- **Encryption**: QUIC provides additional encryption layer on top of Stratum V2's AEAD
- **Multiplexing**: QUIC's native multiplexing supports merge mining channels naturally
- **Feature Flag**: Use `#[cfg(feature = "stratum-v2")]` throughout (like `utxo-commitments` feature)

## Validation Checklist

✅ Transport abstraction pattern validated (UTXO commitments proof)
✅ NetworkManager integration points identified
✅ MiningCoordinator structure supports extension
✅ Configuration system ready for extension
✅ No external dependencies needed (implement from spec)
✅ Protocol details clarified (TLV encoding, message types)
✅ Integration code patterns specified
✅ Iroh support confirmed automatic (via transport abstraction)
✅ File locations and modification points specified
✅ Testing strategy defined

**Plan Status**: ✅ Validated and ready for implementation

