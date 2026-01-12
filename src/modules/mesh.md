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

## API Integration

The module integrates with the node via the Node API IPC protocol:

- **Read-only blockchain access**: Queries blockchain data for payment verification
- **Event subscription**: Receives real-time events from the node (46+ event types)
- **Event publication**: Publishes mesh routing events

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


