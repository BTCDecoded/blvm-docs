# Commons Mesh Module

## Overview

The Commons Mesh module (`blvm-mesh`) implements payment-gated mesh networking for blvm-node. It implements the Commons Mesh routing protocol with fee distribution, traffic classification, and anti-monopoly protection. For information on developing custom modules, see [Module Development](../sdk/module-development.md).

## Features

- **Payment-Gated Routing**: Routes traffic based on payment verification
- **Traffic Classification**: Distinguishes between free and paid traffic
- **Fee Distribution**: Distributes routing fees (60% destination, 30% routers, 10% treasury)
- **Anti-Monopoly Protection**: Prevents single entity from dominating routing
- **Network State Tracking**: Monitors mesh network topology and state

## Installation

### Via Cargo

```bash
cargo install blvm-mesh
```

### Via Module Installer

```bash
cargo install cargo-blvm-module
cargo blvm-module install blvm-mesh
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-mesh.git
   cd blvm-mesh
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/blvm-mesh/target/release
   cp target/release/blvm-mesh /path/to/node/modules/blvm-mesh/target/release/
   ```

## Configuration

Create a `config.toml` file in the module directory:

```toml
[mesh]
# Enable/disable module
enabled = true

# Mesh networking mode
# Options: "bitcoin_only", "payment_gated", "open"
mode = "payment_gated"

# Network listening address
listen_addr = "0.0.0.0:8334"
```

### Configuration Options

- `enabled` (default: `true`): Enable or disable the module
- `mode` (default: `"payment_gated"`): Mesh networking mode
  - `"bitcoin_only"`: Bitcoin-only routing (no payment gating)
  - `"payment_gated"`: Payment-gated routing (default)
  - `"open"`: Open routing (no payment required)
- `listen_addr` (default: `"0.0.0.0:8334"`): Network address to listen on

## Module Manifest

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-mesh"
version = "0.1.0"
description = "Commons Mesh networking module"
author = "Bitcoin Commons Team"
entry_point = "blvm-mesh"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

## Events

### Subscribed Events

The module subscribes to 46+ node events including:

- **Network Events**: `PeerConnected`, `MessageReceived`, `PeerDisconnected`
- **Payment Events**: `PaymentRequestCreated`, `PaymentVerified`, `PaymentSettled`
- **Chain Events**: `NewBlock`, `ChainTipUpdated`, `BlockDisconnected`
- **Mempool Events**: `MempoolTransactionAdded`, `FeeRateChanged`, `MempoolTransactionRemoved`

### Published Events

The module publishes the following events:

- `RouteDiscovered` - Payment route discovered through mesh network
- `RouteFailed` - Payment route discovery failed
- `PaymentVerified` - Payment verified for mesh routing

## Routing Fee Distribution

Mesh routing fees are distributed as follows:

- **60%** to destination node
- **30%** to routing nodes (distributed proportionally)
- **10%** to Commons treasury

## Anti-Monopoly Protection

The module implements anti-monopoly protections to prevent single entities from dominating routing:

- Maximum routing share limits per entity
- Diversification requirements for routing paths
- Fee distribution mechanisms that favor decentralization

## Usage

Once installed and configured, the module automatically:

1. Subscribes to network, payment, chain, and mempool events
2. Classifies traffic as free or paid based on payment verification
3. Routes traffic through the mesh network with payment gating
4. Distributes routing fees according to the fee distribution model
5. Tracks network topology and publishes routing events

## Architecture

### Core Infrastructure

`blvm-mesh` provides the core infrastructure layer for payment-gated routing, while specialized modules build on top for specific use cases. This separation of concerns makes the system composable and allows each module to focus on its domain.

**Repository Structure**: All modules live in the same repository (`blvm-mesh/`) as a Rust workspace. Each submodule is a separate crate that depends on the core `blvm-mesh` library.

**Code**: [BLVM_MESH_MODULAR_ARCHITECTURE.md](https://github.com/BTCDecoded/blvm-node/blob/main/docs/BLVM_MESH_MODULAR_ARCHITECTURE.md)

### Core Components

#### MeshManager

Central coordinator for mesh networking operations:

- **Payment-gated routing**: Routes traffic based on payment verification
- **Protocol detection**: Detects protocol from packet headers
- **Route discovery**: Finds routes through mesh network
- **Replay prevention**: Prevents payment proof replay attacks
- **Payment verification**: Verifies Lightning and CTV payments
- **Routing table management**: Manages mesh network topology

**Code**: [manager.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/manager.rs#L31-L49)

#### PaymentVerifier

Verifies payment proofs for mesh routing:

- **Lightning payments**: Verifies BOLT11 invoices with preimages
- **CTV payments**: Verifies covenant proofs for instant settlement
- **Expiry checking**: Validates payment proof timestamps
- **Amount verification**: Confirms payment amount matches requirements

**Code**: [verifier.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/verifier.rs)

#### RoutingTable

Manages mesh network routing:

- **Direct peers**: Tracks direct connections
- **Multi-hop routes**: Discovers routes through intermediate nodes
- **Fee calculation**: Calculates routing fees (60/30/10 split)
- **Route discovery**: Finds optimal paths through network

**Code**: [routing.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/routing.rs)

#### RoutingPolicyEngine

Determines routing policy based on protocol and configuration:

- **Protocol detection**: Identifies protocol from packet headers
- **Policy determination**: Decides if routing requires payment
- **Mode support**: Bitcoin-only, payment-gated, or open routing

**Code**: [routing_policy.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/routing_policy.rs)

## ModuleAPI

### Overview

`blvm-mesh` exposes a `ModuleAPI` that other modules can call via inter-module IPC. This allows specialized modules to use mesh routing without implementing routing logic themselves.

**Code**: [api.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/api.rs#L66-L134)

### Available Methods

#### `send_packet`

Send a packet through the mesh network.

**Request**:
```rust
pub struct SendPacketRequest {
    pub destination: NodeId,           // 32-byte destination node ID
    pub payload: Vec<u8>,              // Packet payload
    pub payment_proof: Option<PaymentProof>, // Required for paid routing
    pub protocol_id: Option<String>,    // Optional protocol identifier
    pub ttl: Option<u64>,              // Time-to-live (seconds)
}
```

**Response**:
```rust
pub struct SendPacketResponse {
    pub success: bool,
    pub packet_id: [u8; 32],           // Unique packet ID
    pub route_length: usize,            // Number of hops
    pub estimated_cost_sats: u64,       // Total routing cost
    pub error: Option<String>,
}
```

#### `discover_route`

Find a route to a destination node.

**Request**:
```rust
pub struct DiscoverRouteRequest {
    pub destination: NodeId,
    pub max_hops: Option<u8>,          // Maximum route length
    pub timeout_seconds: Option<u64>,   // Discovery timeout
}
```

**Response**:
```rust
pub struct DiscoverRouteResponse {
    pub route: Option<Vec<NodeId>>,    // Route path (None if not found)
    pub route_cost_sats: u64,          // Estimated routing cost
    pub discovery_time_ms: u64,         // Time taken to discover
}
```

#### `register_protocol_handler`

Register a protocol handler for incoming packets.

**Request**:
```rust
pub struct RegisterProtocolRequest {
    pub protocol_id: String,           // e.g., "onion-v1", "mining-pool-v1"
    pub handler_method: String,        // Module method to call when packet arrives
}
```

**Response**:
```rust
pub struct RegisterProtocolResponse {
    pub success: bool,
}
```

#### `get_routing_stats`

Get routing statistics.

**Response**:
```rust
pub struct MeshStats {
    pub enabled: bool,
    pub mode: MeshMode,
    pub routing: RoutingStats,
    pub replay: ReplayStats,
}
```

### Example Module Usage

Specialized modules can use `blvm-mesh` via inter-module IPC:

```rust
// In blvm-onion module
use blvm_node::module::inter_module::api::ModuleAPI;

// Call blvm-mesh ModuleAPI
let mesh_api = module_context.get_module_api("blvm-mesh")?;
let request = SendPacketRequest {
    destination: target_node_id,
    payload: onion_packet,
    payment_proof: Some(payment),
    protocol_id: Some("onion-v1".to_string()),
    ttl: Some(300),
};
let response: SendPacketResponse = mesh_api
    .call_method("send_packet", &request)
    .await?;
```

**Code**: [BLVM_MESH_MODULAR_ARCHITECTURE.md](https://github.com/BTCDecoded/blvm-node/blob/main/docs/BLVM_MESH_MODULAR_ARCHITECTURE.md#blvm-mesh-core-api)

## Example Modules

### blvm-onion

Onion routing module built on top of `blvm-mesh`:

- **Onion packet construction**: Builds multi-layer encrypted packets
- **Route selection**: Chooses random routes through mesh
- **Payment integration**: Uses mesh payment-gated routing
- **Anonymity**: Provides sender/receiver anonymity

**Location**: `blvm-mesh/modules/blvm-onion/`

### blvm-mining-pool

Mining pool coordination module:

- **Pool coordination**: Coordinates mining pool operations
- **Share distribution**: Distributes mining shares via mesh
- **Payment routing**: Uses mesh for pool payments
- **Network discovery**: Discovers pool members via mesh

**Location**: `blvm-mesh/modules/blvm-mining-pool/`

### blvm-messaging

P2P messaging module:

- **Message routing**: Routes messages through mesh network
- **Payment gating**: Uses payment-gated routing for premium messages
- **Protocol handling**: Handles messaging protocol packets
- **Network integration**: Integrates with mesh routing

**Location**: `blvm-mesh/modules/blvm-messaging/`

## API Integration

The module integrates with the node via the Node API IPC protocol:

- **Read-only blockchain access**: Queries blockchain data for payment verification
- **Event subscription**: Receives real-time events from the node (46+ event types)
- **Event publication**: Publishes mesh routing events
- **Inter-module IPC**: Exposes ModuleAPI for other modules to use

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Routing Not Working

- Verify mesh mode is correctly configured
- Check network listening address is accessible
- Verify payment verification is working
- Check node logs for routing errors

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation


