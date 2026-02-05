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

**Available API Operations:**
- `GetBlock`: Get block by hash
- `GetBlockHeader`: Get block header by hash
- `GetTransaction`: Get transaction by hash
- `HasTransaction`: Check if transaction exists
- `GetChainTip`: Get current chain tip hash
- `GetBlockHeight`: Get current block height
- `GetUtxo`: Get UTXO by outpoint (read-only)

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
- `NewBlock`: New block connected to chain
- `NewTransaction`: New transaction in mempool
- `BlockDisconnected`: Block disconnected (chain reorg)
- `ChainReorg`: Chain reorganization occurred
- `PeerConnected`: Peer connected to network
- `PeerDisconnected`: Peer disconnected from network
- `MempoolTransactionAdded`: Transaction added to mempool
- `MempoolTransactionRemoved`: Transaction removed from mempool
- `ConfigLoaded`: Node configuration loaded/changed
- And many more (see [Event System](../architecture/module-system.md#event-system))

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

Modules operate with **whitelist-only access control**. Each module declares required capabilities in its manifest:

- `read_blockchain`: Access to blockchain data
- `read_utxo`: Query UTXO set (read-only)
- `read_chain_state`: Query chain state (height, tip)
- `subscribe_events`: Receive node events (planned)

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

**Node API Operations**: `GetBlock`, `GetBlockHeader`, `GetTransaction`, `HasTransaction`, `GetChainTip`, `GetBlockHeight`, `GetUtxo` (read-only)

**Event Types**: `NewBlock`, `NewTransaction`, `BlockDisconnected`, `ChainReorg`

**Permissions**: `read_blockchain`, `read_utxo`, `read_chain_state`, `subscribe_events`

For detailed API reference, see `blvm-node/src/module/` (traits, IPC protocol, Node API, security).

## See Also

- [SDK Overview](overview.md) - SDK introduction and capabilities
- [SDK API Reference](api-reference.md) - Complete SDK API documentation
- [SDK Examples](examples.md) - Module development examples
- [Module System Architecture](../architecture/module-system.md) - Module system design
- [Module IPC Protocol](../architecture/module-ipc-protocol.md) - IPC communication details
- [Modules Overview](../modules/overview.md) - Available modules
- [Node Configuration](../node/configuration.md) - Configuring modules
