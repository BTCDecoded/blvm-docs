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
- **30%** to routing nodes (distributed proportionally based on route length)
- **10%** to Commons treasury

Fee calculation is performed by the `RoutingTable::calculate_fee()` method, which takes into account:
- Route length (number of hops)
- Base routing cost
- Payment amount (for percentage-based fees)

## Anti-Monopoly Protection

The module implements anti-monopoly protections to prevent single entities from dominating routing:

- **Maximum routing share limits**: Per-entity limits on routing market share
- **Diversification requirements**: Routing paths must include multiple entities
- **Fee distribution mechanisms**: Fee distribution favors decentralized routing paths
- **Route quality scoring**: Routes are scored based on decentralization metrics

These protections are enforced by the `RoutingPolicyEngine` and `RoutingTable` components.

## Usage

Once installed and configured, the module automatically:

1. Subscribes to network, payment, chain, and mempool events
2. Classifies traffic as free or paid based on payment verification
3. Routes traffic through the mesh network with payment gating
4. Distributes routing fees according to the fee distribution model
5. Tracks network topology and publishes routing events

## Architecture

### Core Infrastructure

`blvm-mesh` provides the core infrastructure layer for payment-gated routing. The module exposes a ModuleAPI that allows other modules to build specialized functionality on top of the mesh infrastructure. This separation of concerns makes the system composable and allows each module to focus on its domain.

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

- **Lightning payments**: Verifies BOLT11 invoices with preimages via NodeAPI
- **CTV payments**: Verifies covenant proofs for instant settlement (requires CTV feature flag)
- **Expiry checking**: Validates payment proof timestamps to prevent expired proofs
- **Amount verification**: Confirms payment amount matches routing requirements
- **NodeAPI integration**: Uses NodeAPI to query blockchain for payment verification

**Code**: [verifier.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/verifier.rs)

#### ReplayPrevention

Prevents payment proof replay attacks:

- **Hash-based tracking**: Tracks payment proof hashes to detect replays
- **Sequence numbers**: Uses sequence numbers for additional replay protection
- **Expiry cleanup**: Removes expired payment proof hashes (24-hour expiry)
- **Lock-free reads**: Uses DashMap for concurrent access without blocking

**Code**: [replay.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/replay.rs)

#### RoutingTable

Manages mesh network routing:

- **Direct peers**: Tracks direct connections using DashMap for lock-free concurrent access
- **Multi-hop routes**: Discovers routes through intermediate nodes using distance vector routing
- **Fee calculation**: Calculates routing fees (60/30/10 split) based on route length and payment amount
- **Route discovery**: Finds optimal paths through network with route quality scoring
- **Route expiry**: Routes expire after 1 hour (configurable)
- **Route caching**: Caches discovered routes for performance

**Code**: [routing.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/routing.rs)

#### RouteDiscovery

Implements route discovery protocol:

- **Distance vector routing**: Simple, scalable routing algorithm
- **Route requests**: Broadcasts route requests to find paths
- **Route responses**: Collects route responses from network
- **Route advertisements**: Advertises known routes to neighbors
- **Timeout handling**: 30-second timeout for route discovery
- **Maximum hops**: 10 hops maximum for route discovery

**Code**: [discovery.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/discovery.rs)

#### RoutingPolicyEngine

Determines routing policy based on protocol and configuration:

- **Protocol detection**: Identifies protocol from packet headers
- **Policy determination**: Decides if routing requires payment
- **Mode support**: Bitcoin-only, payment-gated, or open routing

**Code**: [routing_policy.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/routing_policy.rs)

## ModuleAPI

### Overview

`blvm-mesh` exposes a `ModuleAPI` that other modules can call via inter-module IPC. This allows specialized modules to use mesh routing without implementing routing logic themselves.

**Code**: [api.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/api.rs)

### Available Methods

#### `send_packet`

Send a packet through the mesh network.

**Request**: `SendPacketRequest`
- `destination: NodeId` - 32-byte destination node ID
- `payload: Vec<u8>` - Packet payload
- `payment_proof: Option<PaymentProof>` - Required for paid routing
- `protocol_id: Option<String>` - Optional protocol identifier
- `ttl: Option<u64>` - Time-to-live (seconds)

**Response**: `SendPacketResponse`
- `success: bool` - Whether packet was sent successfully
- `packet_id: [u8; 32]` - Unique packet ID
- `route_length: usize` - Number of hops
- `estimated_cost_sats: u64` - Total routing cost
- `error: Option<String>` - Error message if failed

#### `discover_route`

Find a route to a destination node.

**Request**: `DiscoverRouteRequest`
- `destination: NodeId` - Destination node ID
- `max_hops: Option<u8>` - Maximum route length
- `timeout_seconds: Option<u64>` - Discovery timeout

**Response**: `DiscoverRouteResponse`
- `route: Option<Vec<NodeId>>` - Route path (None if not found)
- `route_cost_sats: u64` - Estimated routing cost
- `discovery_time_ms: u64` - Time taken to discover

#### `register_protocol_handler`

Register a protocol handler for incoming packets.

**Request**: `RegisterProtocolRequest`
- `protocol_id: String` - Protocol identifier (e.g., "onion-v1", "mining-pool-v1")
- `handler_method: String` - Module method to call when packet arrives

**Response**: `RegisterProtocolResponse`
- `success: bool` - Whether registration succeeded

#### `get_routing_stats`

Get routing statistics.

**Response**: `MeshStats`
- `enabled: bool` - Whether mesh is enabled
- `mode: MeshMode` - Current mesh mode
- `routing: RoutingStats` - Routing statistics
- `replay: ReplayStats` - Replay prevention statistics

#### `get_node_id`

Get the mesh module's node ID.

**Response**: `NodeId` - 32-byte node ID

## Building on Mesh Infrastructure

The `blvm-mesh` module exposes a ModuleAPI that allows other modules to build specialized functionality on top of the core mesh infrastructure. Specialized modules can use the mesh routing system via inter-module IPC.

### Using the Mesh ModuleAPI

Modules can call the mesh ModuleAPI in two ways:

#### Option 1: Direct NodeAPI Call

```rust
use blvm_node::module::traits::NodeAPI;
use blvm_mesh::api::SendPacketRequest;

// Call mesh module API directly
let request = SendPacketRequest {
    destination: target_node_id,
    payload: packet_data,
    payment_proof: Some(payment),
    protocol_id: Some("onion-v1".to_string()),
    ttl: Some(300),
};
let response_data = node_api
    .call_module(Some("blvm-mesh"), "send_packet", bincode::serialize(&request)?)
    .await?;
let response: SendPacketResponse = bincode::deserialize(&response_data)?;
```

#### Option 2: MeshClient Helper (Recommended)

For convenience, the mesh module provides a `MeshClient` API wrapper that handles serialization:

```rust
use blvm_mesh::MeshClient;

// Create mesh client
let mesh_client = MeshClient::new(node_api, "blvm-mesh".to_string());

// Send packet
let response = mesh_client
    .send_packet("my-module-id", destination, payload, payment_proof, Some("onion-v1".to_string()))
    .await?;

// Discover route
let route = mesh_client
    .discover_route("my-module-id", destination, Some(10))
    .await?;

// Register protocol handler
mesh_client
    .register_protocol_handler("my-module-id", "onion-v1".to_string(), "handle_packet".to_string())
    .await?;
```

**Code**: [client_api.rs](https://github.com/BTCDecoded/blvm-mesh/blob/main/src/client_api.rs)

### Example Use Cases

Specialized modules can be built to use `blvm-mesh` for:

- **Onion Routing**: Multi-layer encrypted packets with anonymous routing (inspired by [Tor Project](https://www.torproject.org/))
- **Mining Pool Coordination**: Decentralized mining pool operations via mesh
- **P2P Messaging**: Payment-gated messaging over mesh network

### Integration Pattern

Any module can integrate with `blvm-mesh` by:

1. **Using MeshClient**: Create a `MeshClient` instance with `MeshClient::new(node_api, "blvm-mesh".to_string())`
2. **Registering a protocol**: Call `mesh_client.register_protocol_handler()` to register a protocol identifier (e.g., `"onion-v1"`, `"mining-pool-v1"`, `"messaging-v1"`)
3. **Sending packets**: Use `mesh_client.send_packet()` to route packets through the mesh network
4. **Discovering routes**: Use `mesh_client.discover_route()` to find routes to destination nodes
5. **Receiving packets**: Handle incoming packets via the registered protocol handler method

### Implementation Details

The mesh module provides both internal routing via `MeshManager` and external API access via `MeshModuleAPI`:

- **Internal routing**: Processes incoming mesh packets via `handle_packet`, routes packets through the mesh network, verifies payments, and manages routing tables
- **External API**: Exposes `MeshModuleAPI` for other modules to call via inter-module IPC, providing methods for sending packets, discovering routes, and registering protocol handlers
- **ModuleIntegration**: Uses the new `ModuleIntegration` API for IPC communication, replacing the old `ModuleClient` and `NodeApiIpc` approach

For detailed information on the mesh implementation, see the [API.md](https://github.com/BTCDecoded/blvm-mesh/blob/main/API.md) documentation. For developing modules that integrate with mesh routing, see [Module Development](../sdk/module-development.md).

## API Integration

The module integrates with the node via `ModuleIntegration`:

- **ModuleIntegration**: Uses `ModuleIntegration::connect()` for IPC communication (replaces old `ModuleClient` and `NodeApiIpc`)
- **NodeAPI access**: Gets NodeAPI via `integration.node_api()` for blockchain queries and payment verification
- **Event subscription**: Subscribes to events via `integration.subscribe_events()` and receives via `integration.event_receiver()`
- **Event publication**: Publishes mesh-specific events via NodeAPI
- **Inter-module IPC**: Exposes ModuleAPI for other modules to call via `node_api.call_module()`

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Routing Not Working

- Verify mesh mode is correctly configured (`bitcoin_only`, `payment_gated`, or `open`)
- Check network listening address is accessible and not blocked by firewall
- Verify payment verification is working (if using payment-gated mode)
- Check node logs for routing errors
- Verify peers are connected and routing table has entries
- Check replay prevention isn't blocking valid packets

### Payment Verification Issues

- Verify Lightning node is accessible (if using Lightning payments)
- Check CTV covenant proofs are valid (if using CTV payments)
- Verify payment proof timestamps are not expired
- Check payment amounts match routing requirements

## Repository

- **GitHub**: [blvm-mesh](https://github.com/BTCDecoded/blvm-mesh)
- **Version**: 0.1.0
- **API Documentation**: [API.md](https://github.com/BTCDecoded/blvm-mesh/blob/main/API.md)

## External Resources

- **Tor Project**: [https://www.torproject.org/](https://www.torproject.org/) - Inspiration for onion routing concepts used in mesh submodules
- **Tor Documentation**: [Tor Project Documentation](https://2019.www.torproject.org/docs/documentation.html.en) - Tor network documentation and technical details

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation


