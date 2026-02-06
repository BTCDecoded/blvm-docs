# Module Development

The BTCDecoded blvm-node includes a process-isolated module system that enables optional features (Lightning, merge mining, privacy enhancements) without affecting consensus or base node stability. Modules run in separate processes with IPC communication, providing security through isolation.

### Core Principles

1. **Process Isolation**: Each module runs in a separate process with isolated memory
2. **API Boundaries**: Modules communicate only through well-defined APIs
3. **Crash Containment**: Module failures don't propagate to the base node
4. **Consensus Isolation**: Modules cannot modify consensus rules, UTXO set, or block validation
5. **State Separation**: Module state is completely separate from consensus state

### Communication

Modules communicate with the node via **Inter-Process Communication (IPC)** using Unix domain sockets. Protocol uses length-delimited binary messages (bincode serialization) with message types: Requests, Responses, Events. Connection is persistent for request/response pattern; events use pub/sub pattern for real-time notifications.

## Module Structure

### Directory Layout

Each module should be placed in a subdirectory within the `modules/` directory:

```
modules/
└── my-module/
    ├── Cargo.toml
    ├── src/
    │   └── main.rs
    └── module.toml          # Module manifest (required)
```

### Module Manifest (`module.toml`)

Every module must include a `module.toml` manifest file:

```toml
# ============================================================================
# Module Manifest
# ============================================================================

# ----------------------------------------------------------------------------
# Core Identity (Required)
# ----------------------------------------------------------------------------
name = "my-module"
version = "1.0.0"
entry_point = "my-module"

# ----------------------------------------------------------------------------
# Metadata (Optional)
# ----------------------------------------------------------------------------
description = "Description of what this module does"
author = "Your Name <your.email@example.com>"

# ----------------------------------------------------------------------------
# Capabilities
# ----------------------------------------------------------------------------
# Permissions this module requires to function
capabilities = [
    "read_blockchain",    # Query blockchain data
    "subscribe_events",   # Receive node events
]

# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
# Required dependencies (module cannot load without these)
[dependencies]
"blvm-lightning" = ">=1.0.0"

# Optional dependencies (module can work without these)
[optional_dependencies]
"blvm-mesh" = ">=0.5.0"

# ----------------------------------------------------------------------------
# Configuration Schema (Optional)
# ----------------------------------------------------------------------------
[config_schema]
poll_interval = "Polling interval in seconds (default: 5)"
```

**Required Fields:**
- `name`: Module identifier (alphanumeric with dashes/underscores)
- `version`: Semantic version (e.g., "1.0.0")
- `entry_point`: Binary name or path

**Optional Fields:**
- `description`: Human-readable description
- `author`: Module author
- `capabilities`: List of required permissions
- `dependencies`: Required (hard) dependencies - module cannot load without them
- `optional_dependencies`: Optional (soft) dependencies - module can work without them

**Dependency Version Constraints:**
- `>=1.0.0` - Greater than or equal to version
- `<=2.0.0` - Less than or equal to version
- `=1.2.3` - Exact version match
- `^1.0.0` - Compatible version (>=1.0.0 and <2.0.0)
- `~1.2.0` - Patch updates only (>=1.2.0 and <1.3.0)

## Module Development

### Basic Module Structure

A minimal module implements the module lifecycle and connects to the node via IPC. There are two approaches:

#### Using ModuleIntegration (Recommended)

```rust
use blvm_node::module::integration::ModuleIntegration;
use blvm_node::module::EventType;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse command-line arguments
    let args = Args::parse();
    
    // Connect to node using ModuleIntegration
    let mut integration = ModuleIntegration::connect(
        args.socket_path,
        args.module_id.unwrap_or_else(|| "my-module".to_string()),
        "my-module".to_string(),
        env!("CARGO_PKG_VERSION").to_string(),
    ).await?;
    
    // Subscribe to events
    let event_types = vec![EventType::NewBlock, EventType::NewTransaction];
    integration.subscribe_events(event_types).await?;
    
    // Get NodeAPI
    let node_api = integration.node_api();
    
    // Get event receiver
    let mut event_receiver = integration.event_receiver();
    
    // Main module loop
    while let Some(event) = event_receiver.recv().await {
        // Handle event
        match event {
            ModuleMessage::Event(event_msg) => {
                // Process event
            }
            _ => {}
        }
    }
    
    Ok(())
}
```

#### Using ModuleClient + NodeApiIpc (Legacy)

```rust
use blvm_node::module::ipc::client::ModuleIpcClient;
use blvm_node::module::api::node_api::NodeApiIpc;
use std::sync::Arc;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse command-line arguments
    let args = Args::parse();
    
    // Connect to node IPC socket
    let mut ipc_client = ModuleIpcClient::connect(&args.socket_path).await?;
    
    // Perform handshake
    // ... handshake code ...
    
    // Create NodeAPI wrapper
    let node_api = Arc::new(NodeApiIpc::new(ipc_client.clone()));
    
    // Create ModuleClient for events
    let mut client = ModuleClient::connect(/* ... */).await?;
    client.subscribe_events(event_types).await?;
    let mut event_receiver = client.event_receiver();
    
    // Main module loop
    while let Some(event) = event_receiver.recv().await {
        // Handle event
    }
    
    Ok(())
}
```

**Recommendation:** New modules should use `ModuleIntegration` for simplicity and consistency. The legacy approach is still supported for existing modules.

### Module Lifecycle

Modules receive command-line arguments (`--module-id`, `--socket-path`, `--data-dir`) and configuration via environment variables (`MODULE_CONFIG_*`). Lifecycle: **Initialization** (connect IPC) → **Start** (subscribe events) → **Running** (process events/requests) → **Stop** (clean shutdown).

### Querying Node Data

Modules can query blockchain data through the Node API:

```rust
// Get current chain tip
let request = RequestMessage {
    correlation_id: client.next_correlation_id(),
    payload: RequestPayload::GetChainTip,
};
let response = client.send_request(request).await?;

// Get a block
let request = RequestMessage {
    correlation_id: client.next_correlation_id(),
    payload: RequestPayload::GetBlock { hash },
};
let response = client.send_request(request).await?;
```

**Available NodeAPI Methods:**

**Blockchain API:**
- `get_block(hash)` - Get block by hash
- `get_block_header(hash)` - Get block header by hash
- `get_transaction(hash)` - Get transaction by hash
- `has_transaction(hash)` - Check if transaction exists
- `get_chain_tip()` - Get current chain tip hash
- `get_block_height()` - Get current block height
- `get_block_by_height(height)` - Get block by height
- `get_utxo(outpoint)` - Get UTXO by outpoint (read-only)
- `get_chain_info()` - Get chain information (tip, height, difficulty, etc.)

**Mempool API:**
- `get_mempool_transactions()` - Get all transaction hashes in mempool
- `get_mempool_transaction(hash)` - Get transaction from mempool by hash
- `get_mempool_size()` - Get mempool size information
- `check_transaction_in_mempool(hash)` - Check if transaction is in mempool
- `get_fee_estimate(target_blocks)` - Get fee estimate for target confirmation blocks

**Network API:**
- `get_network_stats()` - Get network statistics
- `get_network_peers()` - Get list of connected peers

**Storage API:**
- `storage_open_tree(name)` - Open a storage tree (isolated per module)
- `storage_insert(tree_id, key, value)` - Insert a key-value pair
- `storage_get(tree_id, key)` - Get a value by key
- `storage_remove(tree_id, key)` - Remove a key-value pair
- `storage_contains_key(tree_id, key)` - Check if key exists
- `storage_iter(tree_id)` - Iterate over all key-value pairs
- `storage_transaction(tree_id, operations)` - Execute atomic batch of operations

**Filesystem API:**
- `read_file(path)` - Read a file from module's data directory
- `write_file(path, data)` - Write data to a file
- `delete_file(path)` - Delete a file
- `list_directory(path)` - List directory contents
- `create_directory(path)` - Create a directory
- `get_file_metadata(path)` - Get file metadata (size, type, timestamps)

**Module Communication API:**
- `call_module(target_module_id, method, params)` - Call an API method on another module
- `publish_event(event_type, payload)` - Publish an event to other modules
- `register_module_api(api)` - Register module API for other modules to call
- `unregister_module_api()` - Unregister module API
- `discover_modules()` - Discover all available modules
- `get_module_info(module_id)` - Get information about a specific module
- `is_module_available(module_id)` - Check if a module is available

**RPC API:**
- `register_rpc_endpoint(method, description)` - Register a JSON-RPC endpoint
- `unregister_rpc_endpoint(method)` - Unregister an RPC endpoint

**Timers API:**
- `register_timer(interval_seconds, callback)` - Register a periodic timer
- `cancel_timer(timer_id)` - Cancel a registered timer
- `schedule_task(delay_seconds, callback)` - Schedule a one-time task

**Metrics API:**
- `report_metric(metric)` - Report a metric to the node
- `get_module_metrics(module_id)` - Get module metrics
- `get_all_metrics()` - Get aggregated metrics from all modules

**Lightning & Payment API:**
- `get_lightning_node_url()` - Get Lightning node connection info
- `get_lightning_info()` - Get Lightning node information
- `get_payment_state(payment_id)` - Get payment state by payment ID

**Network Integration API:**
- `send_mesh_packet_to_module(module_id, packet_data, peer_addr)` - Send mesh packet to a module

For complete API reference, see [NodeAPI trait](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L150-L450).

### Subscribing to Events

Modules can subscribe to real-time node events. The approach depends on which integration method you're using:

#### Using ModuleIntegration

```rust
// Subscribe to events
let event_types = vec![EventType::NewBlock, EventType::NewTransaction];
integration.subscribe_events(event_types).await?;

// Get event receiver
let mut event_receiver = integration.event_receiver();

// Receive events in main loop
while let Some(event) = event_receiver.recv().await {
    match event {
        ModuleMessage::Event(event_msg) => {
            // Handle event
        }
        _ => {}
    }
}
```

#### Using ModuleClient

```rust
// Subscribe to events
let event_types = vec![EventType::NewBlock, EventType::NewTransaction];
client.subscribe_events(event_types).await?;

// Get event receiver
let mut event_receiver = client.event_receiver();

// Receive events in main loop
while let Some(event) = event_receiver.recv().await {
    match event {
        ModuleMessage::Event(event_msg) => {
            // Handle event
        }
        _ => {}
    }
}
```

**Available Event Types:**

**Core Blockchain Events:**
- `NewBlock` - New block connected to chain
- `NewTransaction` - New transaction in mempool
- `BlockDisconnected` - Block disconnected (chain reorg)
- `ChainReorg` - Chain reorganization occurred

**Payment Events:**
- `PaymentRequestCreated`, `PaymentSettled`, `PaymentFailed`, `PaymentVerified`, `PaymentRouteFound`, `PaymentRouteFailed`, `ChannelOpened`, `ChannelClosed`

**Mining Events:**
- `BlockMined`, `BlockTemplateUpdated`, `MiningDifficultyChanged`, `MiningJobCreated`, `ShareSubmitted`, `MergeMiningReward`, `MiningPoolConnected`, `MiningPoolDisconnected`

**Network Events:**
- `PeerConnected`, `PeerDisconnected`, `PeerBanned`, `MessageReceived`, `MessageSent`, `BroadcastStarted`, `BroadcastCompleted`, `RouteDiscovered`, `RouteFailed`

**Module Lifecycle Events:**
- `ModuleLoaded`, `ModuleUnloaded`, `ModuleCrashed`, `ModuleDiscovered`, `ModuleInstalled`, `ModuleUpdated`, `ModuleRemoved`

**Configuration & Lifecycle Events:**
- `ConfigLoaded`, `NodeStartupCompleted`, `NodeShutdown`, `NodeShutdownCompleted`

**Maintenance & Resource Events:**
- `DataMaintenance`, `MaintenanceStarted`, `MaintenanceCompleted`, `HealthCheck`, `DiskSpaceLow`, `ResourceLimitWarning`

**Governance Events:**
- `GovernanceProposalCreated`, `GovernanceProposalVoted`, `GovernanceProposalMerged`, `EconomicNodeRegistered`, `EconomicNodeVeto`, `VetoThresholdReached`

**Consensus Events:**
- `BlockValidationStarted`, `BlockValidationCompleted`, `ScriptVerificationStarted`, `ScriptVerificationCompleted`, `DifficultyAdjusted`, `SoftForkActivated`

**Mempool Events:**
- `MempoolTransactionAdded`, `MempoolTransactionRemoved`, `FeeRateChanged`

And many more. For complete list, see [EventType enum](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L485-L765) and [Event System](../architecture/module-system.md#event-system).

## Configuration

Module system is configured in node config (see [Node Configuration](../node/configuration.md)):

```toml
[modules]
enabled = true
modules_dir = "modules"
data_dir = "data/modules"
enabled_modules = []  # Empty = auto-discover all

[modules.module_configs.my-module]
setting1 = "value1"
```

Modules can have their own `config.toml` files, passed via environment variables.

## Security Model

### Permissions

Modules operate with **whitelist-only access control**. Each module declares required capabilities in its manifest. Capabilities use snake_case in `module.toml` and map to `Permission` enum variants.

**Core Permissions:**
- `read_blockchain` - Access to blockchain data
- `read_utxo` - Query UTXO set (read-only)
- `read_chain_state` - Query chain state (height, tip)
- `subscribe_events` - Subscribe to node events
- `send_transactions` - Submit transactions to mempool (future: may be restricted)

**Additional Permissions:**
- `read_mempool` - Read mempool data
- `read_network` - Read network data (peers, stats)
- `network_access` - Send network packets
- `read_lightning` - Read Lightning network data
- `read_payment` - Read payment data
- `read_storage`, `write_storage`, `manage_storage` - Storage access
- `read_filesystem`, `write_filesystem`, `manage_filesystem` - Filesystem access
- `register_rpc_endpoint` - Register RPC endpoints
- `manage_timers` - Manage timers and scheduled tasks
- `report_metrics`, `read_metrics` - Metrics access
- `discover_modules` - Discover other modules
- `publish_events` - Publish events to other modules
- `call_module` - Call other modules' APIs
- `register_module_api` - Register module API for other modules to call

For complete list, see [Permission enum](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs#L42-L101).

### Sandboxing

Modules are sandboxed to ensure security:

1. **Process Isolation**: Separate process, isolated memory
2. **File System**: Access limited to module data directory
3. **Network**: No network access (modules can only communicate via IPC)
4. **Resource Limits**: CPU, memory, file descriptor limits (Phase 2+)

### Request Validation

All module API requests are validated:
- Permission checks (module has required permission)
- Consensus protection (no consensus-modifying operations)
- Resource limits (rate limiting, Phase 2+)

## API Reference

**NodeAPI Methods**: See [Querying Node Data](#querying-node-data) section above for complete list of available methods.

**Event Types**: See [Subscribing to Events](#subscribing-to-events) section above for complete list of available event types.

**Permissions**: See [Permissions](#permissions) section above for complete list of available permissions.

For detailed API reference, see:
- [NodeAPI trait](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L150-L450)
- [EventType enum](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L485-L765)
- [Permission enum](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs#L42-L101)

For detailed API reference, see `blvm-node/src/module/` (traits, IPC protocol, Node API, security).

## See Also

- [SDK Overview](overview.md) - SDK introduction and capabilities
- [SDK API Reference](api-reference.md) - Complete SDK API documentation
- [SDK Examples](examples.md) - Module development examples
- [Module System Architecture](../architecture/module-system.md) - Module system design
- [Module IPC Protocol](../architecture/module-ipc-protocol.md) - IPC communication details
- [Modules Overview](../modules/overview.md) - Available modules
- [Node Configuration](../node/configuration.md) - Configuring modules
