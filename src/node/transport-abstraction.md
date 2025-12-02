# Multi-Transport Architecture

## Overview

The transport abstraction layer provides a unified interface for multiple network transport protocols, enabling Bitcoin Commons to support both traditional TCP (Bitcoin P2P compatible) and modern QUIC-based transports simultaneously.

## Architecture

```
NetworkManager
    └── Transport Trait (abstraction)
        ├── TcpTransport (Bitcoin P2P compatible)
        ├── QuinnTransport (direct QUIC)
        └── IrohTransport (QUIC with NAT traversal)
```

## Transport Types

### Transport Comparison

| Feature | TCP | Quinn QUIC | Iroh QUIC |
|---------|-----|------------|-----------|
| **Protocol** | TCP/IP | QUIC | QUIC + DERP |
| **Compatibility** | Bitcoin P2P | Bitcoin P2P compatible | Commons-specific |
| **Addressing** | SocketAddr | SocketAddr | Public Key |
| **NAT Traversal** | ❌ No | ❌ No | ✅ Yes (DERP) |
| **Multiplexing** | ❌ No | ✅ Yes | ✅ Yes |
| **Encryption** | ❌ No (TLS optional) | ✅ Built-in | ✅ Built-in |
| **Connection Migration** | ❌ No | ✅ Yes | ✅ Yes |
| **Latency** | Standard | Lower | Lower |
| **Bandwidth** | Standard | Better | Better |
| **Default** | ✅ Yes | ❌ No | ❌ No |
| **Feature Flag** | Always enabled | `quinn` | `iroh` |

**Code**: ```89:100:bllvm-node/src/network/transport.rs```

### TCP Transport

Traditional TCP transport for Bitcoin P2P protocol compatibility:
- Uses standard TCP sockets
- Maintains Bitcoin wire protocol format
- Compatible with standard Bitcoin nodes
- Default transport for backward compatibility
- No built-in encryption (TLS optional)
- No connection multiplexing

**Code**: ```1:200:bllvm-node/src/network/tcp_transport.rs```

### Quinn QUIC Transport

Direct QUIC transport using the Quinn library:
- QUIC protocol benefits (multiplexing, encryption, connection migration)
- SocketAddr-based addressing (similar to TCP)
- Lower latency and better congestion control
- Built-in TLS encryption
- Stream multiplexing over single connection
- Optional feature flag: `quinn`

**Code**: ```1:200:bllvm-node/src/network/quinn_transport.rs```

### Iroh Transport

QUIC-based transport using Iroh for P2P networking:
- Public key-based peer identity
- NAT traversal support via DERP (Distributed Endpoint Relay Protocol)
- Decentralized peer discovery
- Built-in encryption and multiplexing
- Connection migration support
- Optional feature flag: `iroh`

**Code**: ```1:200:bllvm-node/src/network/iroh_transport.rs```

### Performance Characteristics

**TCP Transport**:
- **Latency**: Standard (RTT-dependent)
- **Throughput**: Standard (TCP congestion control)
- **Connection Overhead**: Low (no encryption by default)
- **Use Case**: Bitcoin P2P compatibility, standard networking

**Quinn QUIC Transport**:
- **Latency**: Lower (0-RTT connection establishment)
- **Throughput**: Higher (better congestion control)
- **Connection Overhead**: Moderate (built-in encryption)
- **Use Case**: Modern applications, improved performance

**Iroh QUIC Transport**:
- **Latency**: Lower (0-RTT + DERP routing)
- **Throughput**: Higher (QUIC + optimized routing)
- **Connection Overhead**: Higher (DERP relay overhead)
- **Use Case**: NAT traversal, decentralized networking

**Code**: ```1:247:bllvm-node/src/network/transport.rs```

## Transport Abstraction

### Transport Trait

The `Transport` trait provides a unified interface:

```rust
pub trait Transport: Send + Sync {
    fn connect(&self, addr: TransportAddr) -> Result<Box<dyn TransportConnection>>;
    fn listen(&self, addr: TransportAddr) -> Result<Box<dyn TransportListener>>;
    fn transport_type(&self) -> TransportType;
}
```

**Code**: ```1:262:bllvm-node/src/network/transport.rs```

### TransportAddr

Unified address type supporting all transports:

```rust
pub enum TransportAddr {
    Tcp(SocketAddr),
    Quinn(SocketAddr),
    Iroh(Vec<u8>), // Public key bytes
}
```

**Code**: ```11:69:bllvm-node/src/network/transport.rs```

### TransportType

Runtime transport selection:

```rust
pub enum TransportType {
    Tcp,
    Quinn,
    Iroh,
}
```

**Code**: ```89:100:bllvm-node/src/network/transport.rs```

## Transport Selection

### Transport Preference

Runtime preference for transport selection:

- **TcpOnly**: Use only TCP transport
- **IrohOnly**: Use only Iroh transport
- **Hybrid**: Prefer Iroh if available, fallback to TCP

**Code**: ```100:162:bllvm-node/src/network/transport.rs```

### Feature Negotiation

Peers negotiate transport capabilities during connection:
- Service flags indicate transport support
- Automatic fallback if preferred transport unavailable
- Transport-aware message routing

**Code**: ```1:200:bllvm-node/src/network/protocol.rs```

## Protocol Adapter

The `ProtocolAdapter` handles message serialization between:
- Consensus-proof `NetworkMessage` types
- Transport-specific wire formats (TCP Bitcoin P2P vs Iroh message format)

**Code**: ```1:200:bllvm-node/src/network/protocol_adapter.rs```

## Message Bridge

The `MessageBridge` bridges blvm-consensus message processing with transport layer:
- Converts messages to/from transport formats
- Processes incoming messages
- Generates responses

**Code**: ```1:200:bllvm-node/src/network/message_bridge.rs```

## Network Manager Integration

The `NetworkManager` supports multiple transports:
- Runtime transport selection
- Transport-aware peer management
- Unified message routing
- Automatic transport fallback

**Code**: ```1:200:bllvm-node/src/network/mod.rs```

## Benefits

1. **Backward Compatibility**: TCP transport maintains Bitcoin P2P compatibility
2. **Modern Protocols**: QUIC support for improved performance
3. **Flexibility**: Runtime transport selection
4. **Unified Interface**: Single API for all transports
5. **NAT Traversal**: Iroh transport enables NAT traversal
6. **Extensible**: Easy to add new transport types

## Usage

### Configuration

```toml
[network]
transport_preference = "Hybrid"  # or "TcpOnly" or "IrohOnly"

[network.tcp]
enabled = true
listen_addr = "0.0.0.0:8333"

[network.iroh]
enabled = true
node_id = "..."
```

### Code Example

```rust
use bllvm_node::network::{NetworkManager, TransportAddr, TransportType};

let network_manager = NetworkManager::new(config);

// Connect via TCP
let tcp_addr = TransportAddr::tcp("127.0.0.1:8333".parse()?);
network_manager.connect(tcp_addr).await?;

// Connect via Iroh
let iroh_addr = TransportAddr::iroh(pubkey_bytes);
network_manager.connect(iroh_addr).await?;
```

## Components

The transport abstraction includes:
- Transport trait definitions
- TCP transport implementation
- Quinn QUIC transport (optional)
- Iroh QUIC transport (optional)
- Protocol adapter for message conversion
- Message bridge for unified routing
- Network manager integration

**Location**: `bllvm-node/src/network/transport.rs`, `bllvm-node/src/network/tcp_transport.rs`, `bllvm-node/src/network/quinn_transport.rs`, `bllvm-node/src/network/iroh_transport.rs`

