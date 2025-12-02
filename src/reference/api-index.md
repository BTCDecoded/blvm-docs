# API Index

Quick reference and cross-references to all BLVM APIs across the ecosystem.

## Complete API Documentation

For detailed Rust API documentation with full type signatures, examples, and implementation details:

- **[bllvm-consensus](https://docs.rs/bllvm-consensus)** - Consensus layer APIs (transaction validation, block validation, script execution)
- **[bllvm-protocol](https://docs.rs/bllvm-protocol)** - Protocol abstraction layer APIs (network variants, message handling)
- **[bllvm-node](https://docs.rs/bllvm-node)** - Node implementation APIs (storage, networking, RPC, modules)
- **[bllvm-sdk](https://docs.rs/bllvm-sdk)** - Developer SDK APIs (governance primitives, composition framework)

## Quick Reference by Component

### Consensus Layer (bllvm-consensus)

**Core Functions:**
- `CheckTransaction` - Validate transaction structure and signatures
- `ConnectBlock` - Validate and connect block to chain
- `EvalScript` - Execute Bitcoin script
- `VerifyScript` - Verify script execution results

**Key Types:**
- `Transaction`, `Block`, `BlockHeader`
- `UTXO`, `OutPoint`
- `Script`, `ScriptOpcode`
- `ValidationResult`

**Documentation:** See [Consensus Overview](../consensus/overview.md), [Consensus Architecture](../consensus/architecture.md), and [Formal Verification](../consensus/formal-verification.md).

### Protocol Layer (bllvm-protocol)

**Core Abstractions:**
- `BitcoinProtocolEngine` - Protocol engine for network variants
- `NetworkMessage` - P2P message types
- `ProtocolVersion` - Network variant (BitcoinV1, Testnet3, Regtest)

**Key Types:**
- `NetworkMessage`, `MessageType`
- `PeerConnection`, `ConnectionState`
- `BlockTemplate` (for mining)

**Documentation:** See [Protocol Overview](../protocol/overview.md), [Network Protocol](../protocol/network-protocol.md), and [Protocol Architecture](../protocol/architecture.md).

### Node Implementation (bllvm-node)

#### Node API

**Main Node Type:**
- `Node` - Main node orchestrator

**Key Methods:**
- `Node::new(protocol_version: Option<ProtocolVersion>) -> Result<Self>` - Create new node
- `Node::start() -> Result<()>` - Start the node
- `Node::stop() -> Result<()>` - Stop the node gracefully

#### Module System API

**NodeAPI Trait** - Interface for modules to query node state:

```rust
pub trait NodeAPI {
    async fn get_block(&self, hash: &Hash) -> Result<Option<Block>, ModuleError>;
    async fn get_block_header(&self, hash: &Hash) -> Result<Option<BlockHeader>, ModuleError>;
    async fn get_transaction(&self, hash: &Hash) -> Result<Option<Transaction>, ModuleError>;
    async fn has_transaction(&self, hash: &Hash) -> Result<bool, ModuleError>;
    async fn get_chain_tip(&self) -> Result<Hash, ModuleError>;
    async fn get_block_height(&self) -> Result<u64, ModuleError>;
    async fn get_utxo(&self, outpoint: &OutPoint) -> Result<Option<UTXO>, ModuleError>;
    async fn subscribe_events(&self, event_types: Vec<EventType>) -> Result<Receiver<ModuleMessage>, ModuleError>;
}
```

**Event Types:**
- `EventType::NewBlock` - New block connected to chain
- `EventType::NewTransaction` - New transaction in mempool
- `EventType::BlockDisconnected` - Block disconnected (chain reorg)
- `EventType::ChainReorg` - Chain reorganization occurred

**ModuleContext** - Context provided to modules:

```rust
pub struct ModuleContext {
    pub module_id: String,
    pub socket_path: String,
    pub data_dir: String,
    pub config: HashMap<String, String>,
}
```

**Documentation:** See [Module Development](../sdk/module-development.md) for complete module API details.

#### RPC API

**RPC Methods:** Bitcoin Core-compatible JSON-RPC methods. See [RPC API Reference](../node/rpc-api.md) for complete list.

**Key Categories:**
- Blockchain methods (8): `getblockchaininfo`, `getblock`, `getblockhash`, `getblockheader`, `getbestblockhash`, `getblockcount`, `getdifficulty`, `gettxoutsetinfo`, `verifychain`
- Raw transaction methods (7): `getrawtransaction`, `sendrawtransaction`, `testmempoolaccept`, `decoderawtransaction`, `gettxout`, `gettxoutproof`, `verifytxoutproof`
- Mempool methods (3): `getmempoolinfo`, `getrawmempool`, `savemempool`
- Network methods (9): `getnetworkinfo`, `getpeerinfo`, `getconnectioncount`, `ping`, `addnode`, `disconnectnode`, `getnettotals`, `clearbanned`, `setban`, `listbanned`
- Mining methods (4): `getmininginfo`, `getblocktemplate`, `submitblock`, `estimatesmartfee`

**Documentation:** See [RPC API Reference](../node/rpc-api.md).

#### Storage API

**Storage Trait:**
- `Storage` - Storage backend interface

**Key Methods:**
- `get_block(&self, hash: &Hash) -> Result<Option<Block>>`
- `get_block_header(&self, hash: &Hash) -> Result<Option<BlockHeader>>`
- `get_utxo(&self, outpoint: &OutPoint) -> Result<Option<UTXO>>`
- `get_chain_tip(&self) -> Result<Hash>`
- `get_block_height(&self) -> Result<u64>`

**Backends:**
- `redb` - Production-ready embedded database (default, see [Storage Backends](../node/storage-backends.md#redb))
- `sled` - Beta fallback option (see [Storage Backends](../node/storage-backends.md#sled))

**Documentation:** See [Storage Backends](../node/storage-backends.md) and [Node Configuration](../node/configuration.md#storage-backends).

### Developer SDK (bllvm-sdk)

#### Governance Primitives

**Core Types:**
- `GovernanceKeypair` - Keypair for signing
- `PublicKey` - Public key (secp256k1)
- `Signature` - Cryptographic signature
- `GovernanceMessage` - Message types (Release, ModuleApproval, BudgetDecision)
- `Multisig` - Threshold signature configuration

**Functions:**
- `sign_message(secret_key: &SecretKey, message: &[u8]) -> GovernanceResult<Signature>`
- `verify_signature(signature: &Signature, message: &[u8], public_key: &PublicKey) -> GovernanceResult<bool>`

**Documentation:** See [SDK API Reference](../sdk/api-reference.md#governance-primitives).

#### Composition Framework

**Core Types:**
- `ModuleRegistry` - Module discovery and management
- `NodeComposer` - Node composition from modules
- `ModuleLifecycle` - Module lifecycle management
- `NodeSpec`, `ModuleSpec` - Composition specifications

**Documentation:** See [SDK API Reference](../sdk/api-reference.md#composition-framework).

## API Usage Patterns

### Consensus Validation

```rust
use bllvm_consensus::{CheckTransaction, ConnectBlock, Transaction, Block};

// Validate transaction
let result = CheckTransaction::validate(&tx, &utxo_set)?;

// Validate and connect block
let result = ConnectBlock::validate_and_connect(&block, &chain_state)?;
```

### Protocol Abstraction

```rust
use bllvm_protocol::{BitcoinProtocolEngine, ProtocolVersion};

// Create protocol engine for testnet
let engine = BitcoinProtocolEngine::new(ProtocolVersion::Testnet3)?;
```

### Module Development

```rust
use bllvm_node::module::traits::NodeAPI;

// In module code, use NodeAPI trait through IPC
let block = node_api.get_block(&hash).await?;
let tip = node_api.get_chain_tip().await?;
```

### Governance Operations

```rust
use bllvm_sdk::{GovernanceKeypair, GovernanceMessage, Multisig};

// Generate keypair and sign message
let keypair = GovernanceKeypair::generate()?;
let message = GovernanceMessage::Release { version, commit_hash };
let signature = sign_message(&keypair.secret_key_bytes(), &message.to_signing_bytes())?;
```

## API Stability

**Stable APIs:**
- Consensus layer (`bllvm-consensus`) - Stable, formally verified
- Protocol layer (`bllvm-protocol`) - Stable, Bitcoin-compatible
- Node storage APIs - Stable

**Development APIs:**
- Module system APIs - Stable interface, implementation may evolve
- Composition framework - Active development
- Experimental features - Subject to change

## Error Handling

All APIs use consistent error types:
- `bllvm_consensus::ConsensusError` - Consensus validation errors
- `bllvm_protocol::ProtocolError` - Protocol layer errors
- `bllvm_node::module::ModuleError` - Module system errors
- `bllvm_sdk::GovernanceError` - Governance operation errors

## See Also

- [SDK API Reference](../sdk/api-reference.md) - Detailed SDK documentation
- [Module Development](../sdk/module-development.md) - Module API usage
- [RPC API Reference](../node/rpc-api.md) - RPC method documentation
- [Configuration Reference](configuration-reference.md) - Configuration APIs
