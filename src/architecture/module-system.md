# Module System

## Overview

The module system supports optional features ([Lightning Network](../modules/lightning.md), [merge mining](../node/mining-stratum-v2.md), privacy enhancements) without affecting consensus or base node stability. Modules run in separate processes with [IPC communication](module-ipc-protocol.md), providing security through isolation.

## Available Modules

The following modules are available for blvm-node:

- **[Lightning Network Module](../modules/lightning.md)** - Lightning Network payment processing, invoice verification, payment routing, and channel management
- **[Commons Mesh Module](../modules/mesh.md)** - Payment-gated mesh networking with routing fees, traffic classification, and anti-monopoly protection
- **[Stratum V2 Module](../modules/stratum-v2.md)** - Stratum V2 mining protocol support and mining pool management
- **[Datum Module](../modules/datum.md)** - DATUM Gateway mining protocol
- **[Mining OS Module](../modules/miningos.md)** - MiningOS integration
- **[Merge Mining Module](../modules/stratum-v2.md)** - Merge mining available as separate paid plugin (`blvm-merge-mining`)

For detailed documentation on each module, see the [Modules](../modules/overview.md) section.

## Architecture

### Process Isolation

Each module runs in a separate process with isolated memory. The base node consensus state is protected and read-only to modules.

```mermaid
graph TB
    subgraph "blvm-node Process"
        CS[Consensus State<br/>Protected, Read-Only]
        MM[Module Manager<br/>Orchestration]
        NM[Network Manager]
        SM[Storage Manager]
        RM[RPC Manager]
    end
    
    subgraph "Module Process 1<br/>blvm-lightning"
        LS[Lightning State<br/>Isolated Memory]
        SB1[Sandbox<br/>Resource Limits]
    end
    
    subgraph "Module Process 2<br/>blvm-mesh"
        MS[Mesh State<br/>Isolated Memory]
        SB2[Sandbox<br/>Resource Limits]
    end
    
    subgraph "Module Process 3<br/>blvm-stratum-v2"
        SS[Stratum V2 State<br/>Isolated Memory]
        SB3[Sandbox<br/>Resource Limits]
    end
    
    MM -->|IPC Unix Sockets| LS
    MM -->|IPC Unix Sockets| MS
    MM -->|IPC Unix Sockets| SS
    
    CS -.->|Read-Only Access| MM
    NM --> MM
    SM --> MM
    RM --> MM
    
    style CS fill:#fbb,stroke:#333,stroke-width:3px
    style MM fill:#bbf,stroke:#333,stroke-width:2px
    style LS fill:#bfb,stroke:#333,stroke-width:2px
    style MS fill:#bfb,stroke:#333,stroke-width:2px
    style SS fill:#bfb,stroke:#333,stroke-width:2px
```

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/mod.rs#L1-L37)

## Core Components

### ModuleManager

Orchestrates all modules, handling lifecycle, runtime loading/unloading/reloading, and coordination.

**Features:**
- Module discovery and loading
- Process spawning and monitoring
- IPC server management
- Event subscription management
- Dependency resolution
- Registry integration

**Code**: [manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/manager.rs#L1-L520)

### Process Isolation

Modules run in separate processes via `ModuleProcessSpawner`:

- Separate memory space
- Isolated execution environment
- Resource limits enforced
- Crash containment

**Code**: [spawner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/process/spawner.rs#L1-L132)

### IPC Communication

Modules communicate with the base node via Unix domain sockets (Unix) or named pipes (Windows):

- Request/response protocol
- Event subscription system
- Correlation IDs for async operations
- Type-safe message serialization

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L1-L234)

### Security Sandbox

Modules run in sandboxed environments with:

- Resource limits (CPU, memory, file descriptors)
- Filesystem restrictions
- Network restrictions
- Permission-based API access

**Code**: [network.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/sandbox/network.rs#L1-L60)

### Permission System

Modules request capabilities that are validated before API access. Capabilities use snake_case in `module.toml` (e.g., `read_blockchain`) and map to `Permission` enum variants (e.g., `ReadBlockchain`).

**Core Permissions:**
- `read_blockchain` / `ReadBlockchain` - Read-only blockchain access (blocks, headers, transactions)
- `read_utxo` / `ReadUTXO` - Query UTXO set (read-only)
- `read_chain_state` / `ReadChainState` - Query chain state (height, tip)
- `subscribe_events` / `SubscribeEvents` - Subscribe to node events
- `send_transactions` / `SendTransactions` - Submit transactions to mempool (future: may be restricted)

**Mempool & Network Permissions:**
- `read_mempool` / `ReadMempool` - Read mempool data (transactions, size, fee estimates)
- `read_network` / `ReadNetwork` - Read network data (peers, stats)
- `network_access` / `NetworkAccess` - Send network packets (mesh packets, etc.)

**Lightning & Payment Permissions:**
- `read_lightning` / `ReadLightning` - Read Lightning network data
- `read_payment` / `ReadPayment` - Read payment data

**Storage Permissions:**
- `read_storage` / `ReadStorage` - Read from module storage
- `write_storage` / `WriteStorage` - Write to module storage
- `manage_storage` / `ManageStorage` - Manage storage (create/delete trees, manage quotas)

**Filesystem Permissions:**
- `read_filesystem` / `ReadFilesystem` - Read files from module data directory
- `write_filesystem` / `WriteFilesystem` - Write files to module data directory
- `manage_filesystem` / `ManageFilesystem` - Manage filesystem (create/delete directories, manage quotas)

**RPC & Timers Permissions:**
- `register_rpc_endpoint` / `RegisterRpcEndpoint` - Register RPC endpoints
- `manage_timers` / `ManageTimers` - Manage timers and scheduled tasks

**Metrics Permissions:**
- `report_metrics` / `ReportMetrics` - Report metrics
- `read_metrics` / `ReadMetrics` - Read metrics

**Module Communication Permissions:**
- `discover_modules` / `DiscoverModules` - Discover other modules
- `publish_events` / `PublishEvents` - Publish events to other modules
- `call_module` / `CallModule` - Call other modules' APIs
- `register_module_api` / `RegisterModuleApi` - Register module API for other modules to call

**Code**: [permissions.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs#L1-L184)

## Module Lifecycle

```
Discovery → Verification → Loading → Execution → Monitoring
    │            │            │           │            │
    │            │            │           │            │
    ▼            ▼            ▼           ▼            ▼
Registry    Signer      Loader      Process      Monitor
```

### Discovery

Modules discovered through:
- Local filesystem (`modules/` directory)
- Module registry (REST API)
- Manual installation

**Code**: [discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/registry/discovery.rs#L1-L200)

### Verification

Each module verified through:
- Hash verification (binary integrity)
- Signature verification (multisig maintainer signatures)
- Permission checking (capability validation)
- Compatibility checking (version requirements)

**Code**: [manifest_validator.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/validation/manifest_validator.rs#L1-L200)

### Loading

Module loaded into isolated process:
- Sandbox creation (resource limits)
- IPC connection establishment
- API subscription setup

**Code**: [manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/manager.rs#L159-L235)

### Execution

Module runs in isolated process:
- Separate memory space
- Resource limits enforced
- IPC communication only
- Event subscription active

### Monitoring

Module health monitored:
- Process status tracking
- Resource usage monitoring
- Error tracking
- Crash isolation

**Code**: [monitor.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/process/monitor.rs#L1-L100)

## Security Model

### Consensus Isolation

Modules cannot:
- Modify consensus rules
- Modify UTXO set
- Access node private keys
- Bypass security boundaries
- Affect other modules

**Guarantee**: Module failures are isolated and cannot affect consensus.

### Crash Containment

Module crashes are isolated and do not affect the base node. The `ModuleProcessMonitor` detects crashes and automatically removes failed modules.

**Code**: [manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/manager.rs#L144-L153)

### Security Flow

```
Module Binary
    │
    ├─→ Hash Verification ──→ Integrity Check
    │
    ├─→ Signature Verification ──→ Multisig Check ──→ Maintainer Verification
    │
    ├─→ Permission Check ──→ Capability Validation
    │
    └─→ Sandbox Creation ──→ Resource Limits ──→ Isolation
```

## Module Manifest

Module manifests use TOML format:

```toml
# Module Identity
name = "lightning-network"
version = "1.2.3"
description = "Lightning Network implementation"
author = "Alice <alice@example.com>"

# Governance
[governance]
tier = "application"
maintainers = ["alice", "bob", "charlie"]
threshold = "2-of-3"
review_period_days = 14

# Signatures
[signatures]
maintainers = [
    { name = "alice", key = "02abc...", signature = "..." },
    { name = "bob", key = "03def...", signature = "..." }
]
threshold = "2-of-3"

# Binary
[binary]
hash = "sha256:abc123..."
size = 1234567
download_url = "https://registry.bitcoincommons.org/modules/lightning-network/1.2.3"

# Dependencies
[dependencies]
"blvm-node" = ">=1.0.0"
"another-module" = ">=0.5.0"

# Compatibility
[compatibility]
min_consensus_version = "1.0.0"
min_protocol_version = "1.0.0"
min_node_version = "1.0.0"
tested_with = ["1.0.0", "1.1.0"]

# Capabilities
capabilities = [
    "read_blockchain",
    "subscribe_events"
]
```

**Code**: [manifest.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/registry/manifest.rs#L1-L200)

## API Hub

The `ModuleApiHub` routes API requests from modules to the appropriate handlers:

- Blockchain API (blocks, headers, transactions)
- Governance API (proposals, votes)
- Communication API (P2P messaging)

**Code**: [hub.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/api/hub.rs#L1-L200)

## Event System

The module event system provides a comprehensive, consistent, and reliable way for modules to receive notifications about node state changes, blockchain events, and system lifecycle events.

### Event Subscription

Modules subscribe to events they need during initialization:

```rust
let event_types = vec![
    EventType::NewBlock,
    EventType::NewTransaction,
    EventType::ModuleLoaded,
    EventType::ConfigLoaded,
];
client.subscribe_events(event_types).await?;
```

### Event Categories

**Core Blockchain Events:**
- `NewBlock` - Block connected to chain
- `NewTransaction` - Transaction in mempool
- `BlockDisconnected` - Block disconnected (reorg)
- `ChainReorg` - Chain reorganization

**Payment Events:**
- `PaymentRequestCreated` - Payment request created
- `PaymentSettled` - Payment settled (confirmed on-chain)
- `PaymentFailed` - Payment failed
- `PaymentVerified` - Lightning payment verified
- `PaymentRouteFound` - Payment route discovered
- `PaymentRouteFailed` - Payment routing failed
- `ChannelOpened` - Lightning channel opened
- `ChannelClosed` - Lightning channel closed

**Mining Events:**
- `BlockMined` - Block mined successfully
- `BlockTemplateUpdated` - Block template updated
- `MiningDifficultyChanged` - Mining difficulty changed
- `MiningJobCreated` - Mining job created
- `ShareSubmitted` - Mining share submitted
- `MergeMiningReward` - Merge mining reward received
- `MiningPoolConnected` - Mining pool connected
- `MiningPoolDisconnected` - Mining pool disconnected

**Mesh Networking Events:**
- `MeshPacketReceived` - Mesh packet received from network

**Stratum V2 Events:**
- `StratumV2MessageReceived` - Stratum V2 message received from network

**Module Lifecycle Events:**
- `ModuleLoaded` - Module loaded (published after subscription)
- `ModuleUnloaded` - Module unloaded
- `ModuleCrashed` - Module crashed
- `ModuleDiscovered` - Module discovered
- `ModuleInstalled` - Module installed
- `ModuleUpdated` - Module updated
- `ModuleRemoved` - Module removed

**Configuration Events:**
- `ConfigLoaded` - Node configuration loaded/changed

**Node Lifecycle Events:**
- `NodeStartupCompleted` - Node fully operational
- `NodeShutdown` - Node shutting down
- `NodeShutdownCompleted` - Shutdown complete

**Maintenance Events:**
- `DataMaintenance` - Unified cleanup/flush event (replaces StorageFlush + DataCleanup)
- `MaintenanceStarted` - Maintenance started
- `MaintenanceCompleted` - Maintenance completed
- `HealthCheck` - Health check performed

**Resource Management Events:**
- `DiskSpaceLow` - Disk space low
- `ResourceLimitWarning` - Resource limit warning

**Governance Events:**
- `GovernanceProposalCreated` - Proposal created
- `GovernanceProposalVoted` - Vote cast
- `GovernanceProposalMerged` - Proposal merged
- `EconomicNodeRegistered` - Economic node registered
- `EconomicNodeStatus` - Economic node status query/response
- `EconomicNodeForkDecision` - Economic node fork decision
- `EconomicNodeVeto` - Economic node veto signal
- `VetoThresholdReached` - Veto threshold reached
- `GovernanceForkDetected` - Governance fork detected
- `WebhookSent` - Webhook sent
- `WebhookFailed` - Webhook delivery failed

**Network Events:**
- `PeerConnected` - Peer connected
- `PeerDisconnected` - Peer disconnected
- `PeerBanned` - Peer banned
- `PeerUnbanned` - Peer unbanned
- `MessageReceived` - Network message received
- `MessageSent` - Network message sent
- `BroadcastStarted` - Broadcast started
- `BroadcastCompleted` - Broadcast completed
- `RouteDiscovered` - Route discovered
- `RouteFailed` - Route failed
- `ConnectionAttempt` - Connection attempt (success/failure)
- `AddressDiscovered` - New peer address discovered
- `AddressExpired` - Peer address expired
- `NetworkPartition` - Network partition detected
- `NetworkReconnected` - Network partition reconnected
- `DoSAttackDetected` - DoS attack detected
- `RateLimitExceeded` - Rate limit exceeded

**Consensus Events:**
- `BlockValidationStarted` - Block validation started
- `BlockValidationCompleted` - Block validation completed (success/failure)
- `ScriptVerificationStarted` - Script verification started
- `ScriptVerificationCompleted` - Script verification completed
- `UTXOValidationStarted` - UTXO validation started
- `UTXOValidationCompleted` - UTXO validation completed
- `DifficultyAdjusted` - Network difficulty adjusted
- `SoftForkActivated` - Soft fork activated (SegWit, Taproot, CTV, etc.)
- `SoftForkLockedIn` - Soft fork locked in (BIP9)
- `ConsensusRuleViolation` - Consensus rule violation detected

**Sync Events:**
- `HeadersSyncStarted` - Headers sync started
- `HeadersSyncProgress` - Headers sync progress update
- `HeadersSyncCompleted` - Headers sync completed
- `BlockSyncStarted` - Block sync started (IBD)
- `BlockSyncProgress` - Block sync progress update
- `BlockSyncCompleted` - Block sync completed

**Mempool Events:**
- `MempoolTransactionAdded` - Transaction added to mempool
- `MempoolTransactionRemoved` - Transaction removed from mempool
- `FeeRateChanged` - Fee rate changed

**Additional Event Categories:**
- Dandelion++ Events (DandelionStemStarted, DandelionStemAdvanced, DandelionFluffed, etc.)
- Compact Blocks Events (CompactBlockReceived, BlockReconstructionStarted, etc.)
- FIBRE Events (FibreBlockEncoded, FibreBlockSent, FibrePeerRegistered)
- Package Relay Events (PackageReceived, PackageRejected)
- UTXO Commitments Events (UtxoCommitmentReceived, UtxoCommitmentVerified)
- Ban List Sharing Events (BanListShared, BanListReceived)

For a complete list of all event types, see [EventType enum](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L485-L765).

### Event Delivery Guarantees

**At-Most-Once Delivery:**
- Events are delivered at most once per subscriber
- If channel is full, event is dropped (not retried)
- If channel is closed, module is removed from subscriptions

**Best-Effort Delivery:**
- Events are delivered on a best-effort basis
- No guaranteed delivery (modules can be slow/dead)
- Statistics track delivery success/failure rates

**Ordering Guarantees:**
- Events are delivered in order per module (single channel)
- No cross-module ordering guarantees
- ModuleLoaded events are ordered: subscription → ModuleLoaded

### Event Timing and Consistency

**ModuleLoaded Event Timing:**
- `ModuleLoaded` events are **only published AFTER a module has subscribed** (after startup is complete)
- This ensures modules are fully ready before receiving ModuleLoaded events
- Hotloaded modules automatically receive all already-loaded modules when subscribing

**Event Flow:**
1. Module process is spawned
2. Module connects via IPC and sends Handshake
3. Module sends `SubscribeEvents` request
4. **At subscription time**:
   - Module receives `ModuleLoaded` events for all already-loaded modules (hotloaded modules get existing modules)
   - `ModuleLoaded` is published for the newly subscribing module (if it's loaded)
5. Module is now fully operational

### Event Delivery Reliability

**Channel Buffering:**
- 100-event buffer per module (prevents unbounded memory growth)
- Non-blocking delivery (publisher never blocks)
- Channel full events are tracked in statistics

**Error Handling:**
- **Channel Full**: Event dropped with warning, module subscription NOT removed (module is slow, not dead)
- **Channel Closed**: Module subscription removed, statistics track failed delivery
- **Serialization Errors**: Event dropped with warning, module subscription NOT removed

**Delivery Statistics:**
- Track success/failure/channel-full counts per module
- Available via `EventManager::get_delivery_stats()`
- Useful for monitoring and debugging

**Code**: [events.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/api/events.rs#L1-L274)

For detailed event system documentation, see:
- [Event System Integration](event-system-integration.md) - Complete integration guide
- [Event Consistency](event-consistency.md) - Event timing and consistency guarantees
- [Janitorial Events](janitorial-events.md) - Maintenance and lifecycle events

## Module Registry

Modules can be discovered and installed from a module registry:

- REST API client for module discovery
- Binary download and verification
- Dependency resolution
- Signature verification

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/registry/client.rs#L1-L200)

## Usage

### Loading a Module

```rust
use blvm_node::module::{ModuleManager, ModuleMetadata};

let mut manager = ModuleManager::new(
    modules_dir,
    data_dir,
    socket_dir,
);

manager.start(socket_path, node_api).await?;

manager.load_module(
    "lightning-network",
    binary_path,
    metadata,
    config,
).await?;
```

### Auto-Discovery

```rust
// Automatically discover and load all modules
manager.auto_load_modules().await?;
```

**Code**: [manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/manager.rs#L306-L391)

## Benefits

1. **Consensus Isolation**: Modules cannot affect consensus rules
2. **Crash Containment**: Module failures don't affect base node
3. **Security**: Process isolation and permission system
4. **Extensibility**: Add features without consensus changes
5. **Flexibility**: Load/unload modules at runtime
6. **Governance**: Modules subject to governance approval

## Use Cases

- **Lightning Network**: Payment channel management
- **Merge Mining**: Auxiliary chain support
- **Privacy Enhancements**: Transaction mixing, coinjoin
- **Alternative Mempool Policies**: Custom transaction selection
- **Smart Contracts**: Layer 2 contract execution

## Components

The module system includes:
- Process isolation
- IPC communication
- Security sandboxing
- Permission system
- Module registry
- Event system
- API hub

**Location**: `blvm-node/src/module/`

## IPC Communication

Modules communicate with the node via the Module IPC Protocol:

- **Protocol**: Length-delimited binary messages over Unix domain sockets
- **Message Types**: Requests, Responses, Events, Logs
- **Security**: Process isolation, permission-based API access, resource sandboxing
- **Performance**: Persistent connections, concurrent requests, correlation IDs

### Integration Approaches

There are two approaches for modules to integrate with the node:

#### 1. ModuleIntegration (Recommended for New Modules)

The `ModuleIntegration` API provides a simplified, unified interface for module integration:

```rust
use blvm_node::module::integration::ModuleIntegration;

// Connect to node
let mut integration = ModuleIntegration::connect(
    socket_path,
    module_id,
    module_name,
    version,
).await?;

// Subscribe to events
integration.subscribe_events(event_types).await?;

// Get NodeAPI
let node_api = integration.node_api();

// Get event receiver
let mut event_receiver = integration.event_receiver();
```

**Benefits:**
- Single unified API for all integration needs
- Automatic handshake and connection management
- Simplified event subscription
- Direct access to NodeAPI and event receiver

**Used by:** `blvm-mesh` and its submodules (`blvm-onion`, `blvm-mining-pool`, `blvm-messaging`, `blvm-bridge`)

#### 2. ModuleClient + NodeApiIpc (Legacy Approach)

The traditional approach uses separate components:

```rust
use blvm_node::module::ipc::client::ModuleIpcClient;
use blvm_node::module::api::node_api::NodeApiIpc;

// Connect to IPC socket
let mut ipc_client = ModuleIpcClient::connect(&socket_path).await?;

// Perform handshake manually
let handshake_request = RequestMessage { /* ... */ };
let response = ipc_client.request(handshake_request).await?;

// Create NodeAPI wrapper
let node_api = Arc::new(NodeApiIpc::new(ipc_client.clone()));

// Create ModuleClient for event subscription
let mut client = ModuleClient::connect(/* ... */).await?;
client.subscribe_events(event_types).await?;
let mut event_receiver = client.event_receiver();
```

**Benefits:**
- More granular control over IPC communication
- Direct access to IPC client for custom requests
- Established, stable API

**Used by:** `blvm-lightning`, `blvm-stratum-v2`, `blvm-datum`, `blvm-miningos`

**Migration:** New modules should use `ModuleIntegration`. Existing modules can continue using `ModuleClient` + `NodeApiIpc`, but migration to `ModuleIntegration` is recommended for consistency and simplicity.

For detailed protocol documentation, see [Module IPC Protocol](module-ipc-protocol.md).

## See Also

- [Module IPC Protocol](module-ipc-protocol.md) - Complete IPC protocol documentation
- [Modules Overview](../modules/overview.md) - Overview of all available modules
- [Lightning Network Module](../modules/lightning.md) - Lightning Network payment processing
- [Commons Mesh Module](../modules/mesh.md) - Payment-gated mesh networking
- [Stratum V2 Module](../modules/stratum-v2.md) - Stratum V2 mining protocol
- [Datum Module](../modules/datum.md) - DATUM Gateway mining protocol
- [Mining OS Module](../modules/miningos.md) - MiningOS integration
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules

