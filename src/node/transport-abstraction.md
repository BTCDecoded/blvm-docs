# Transport abstraction

> **Platform / build** — **Iroh** is in **`blvm` default features** (Linux x86_64 release artifacts use the same default set; portable Windows/aarch64 CI omits several defaults). **Quinn** requires the `quinn` feature (source build). All release binaries default to TCP-capable builds; set `transport_preference` in config. See [Release process — Build variants](../development/release-process.md#build-variants).

## Overview

Multiple network transport protocols (TCP for Bitcoin P2P compatibility and QUIC) share one abstraction so the node can run both at once.

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


### TCP Transport

Traditional TCP transport for Bitcoin P2P protocol compatibility:
- Uses standard TCP sockets
- Maintains Bitcoin wire protocol format
- Compatible with standard Bitcoin nodes
- Default transport for backward compatibility
- No built-in encryption (TLS optional)
- No connection multiplexing


### Quinn QUIC Transport

Direct QUIC transport using the Quinn library:
- QUIC protocol benefits (multiplexing, encryption, connection migration)
- SocketAddr-based addressing (similar to TCP)
- Lower latency and better congestion control
- Built-in TLS encryption
- Stream multiplexing over single connection
- Optional feature flag: `quinn`


### Iroh Transport

QUIC-based transport using Iroh for P2P networking:
- Public key-based peer identity
- NAT traversal support via DERP (Distributed Endpoint Relay Protocol)
- Decentralized peer discovery
- Built-in encryption and multiplexing
- Connection migration support
- Optional feature flag: `iroh`


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


## Transport Abstraction

### Transport Trait

The `Transport` trait is the shared interface:

```rust
pub trait Transport: Send + Sync {
    fn connect(&self, addr: TransportAddr) -> Result<Box<dyn TransportConnection>>;
    fn listen(&self, addr: TransportAddr) -> Result<Box<dyn TransportListener>>;
    fn transport_type(&self) -> TransportType;
}
```


### TransportAddr

Unified address type supporting all transports:

```rust
pub enum TransportAddr {
    Tcp(SocketAddr),
    Quinn(SocketAddr),
    Iroh(Vec<u8>), // Public key bytes
}
```


### TransportType

Runtime transport selection:

```rust
pub enum TransportType {
    Tcp,
    Quinn,
    Iroh,
}
```


## Transport Selection

### Transport Preference

Runtime preference for transport selection:

- **TcpOnly**: Use only TCP transport
- **IrohOnly**: Use only Iroh transport
- **Hybrid**: Prefer Iroh if available, fallback to TCP


### Feature Negotiation

Peers negotiate transport capabilities during connection:
- Service flags indicate transport support
- Automatic fallback if preferred transport unavailable
- Transport-aware message routing


## Protocol Adapter

The `ProtocolAdapter` handles message serialization between:
- Consensus-proof `NetworkMessage` types
- Transport-specific wire formats (TCP Bitcoin P2P vs Iroh message format)


## Message Bridge

The `MessageBridge` bridges blvm-consensus message processing with transport layer:
- Converts messages to/from transport formats
- Processes incoming messages
- Generates responses


## Network Manager Integration

The `NetworkManager` supports multiple transports:
- Runtime transport selection
- Transport-aware peer management
- Unified message routing
- Automatic transport fallback


## Benefits

1. **Backward Compatibility**: TCP transport maintains Bitcoin P2P compatibility
2. **Modern Protocols**: QUIC support for improved performance
3. **Flexibility**: Runtime transport selection
4. **Unified Interface**: Single API for all transports
5. **NAT Traversal**: Iroh transport enables NAT traversal
6. **Extensible**: Easy to add new transport types

## Usage

### Configuration

`NodeConfig` uses **top-level** keys (see [`config/mod.rs`](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs), [`TransportPreferenceConfig`](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs)). Example:

```toml
listen_addr = "0.0.0.0:8333"
transport_preference = "hybrid"   # TOML serde: tcponly | irohonly | quinnonly | hybrid | all
```

P2P listen address is **`listen_addr`**, not a nested `[network.tcp]` table. **`quinn`** / **`iroh`** must be enabled in the binary for non-TCP preferences to work.

### Code Example

[`TransportAddr`](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/transport.rs) wraps TCP / optional Quinn / optional Iroh addresses. Wire-up is via [`NetworkManager`](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs) and the running node — see crate examples and integration tests rather than copying a minimal `new`/`connect` snippet here.

## Components

The transport abstraction includes:
- Transport trait definitions
- TCP transport implementation
- Quinn QUIC transport (optional)
- Iroh QUIC transport (optional)
- Protocol adapter for message conversion
- Message bridge for unified routing
- Network manager integration

## Source

- [transport.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/transport.rs)
- [tcp_transport.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/tcp_transport.rs)
- [quinn_transport.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/quinn_transport.rs)
- [iroh_transport.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/iroh_transport.rs)
- [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/protocol.rs)
- [protocol_adapter.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/protocol_adapter.rs)
- [message_bridge.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/message_bridge.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs)

