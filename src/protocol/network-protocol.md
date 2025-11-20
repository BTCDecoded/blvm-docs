# Network Protocol

The protocol layer abstracts Bitcoin's P2P network protocol, enabling support for multiple network variants.

## Protocol Abstraction

The bllvm-protocol provides abstraction for P2P message formats (standard Bitcoin wire protocol), connection management, peer discovery, block synchronization, and transaction relay.

## Network Variants

### Mainnet (BitcoinV1)
- Production Bitcoin network
- Full consensus rules
- Real economic value

### Testnet3
- Bitcoin test network
- Same consensus rules as mainnet
- Different network parameters
- No real economic value

### Regtest
- Regression testing network
- Configurable difficulty
- Isolated from other networks
- Fast block generation for testing

For implementation details, see the [bllvm-protocol README](../../modules/bllvm-protocol/README.md).

## Transport Abstraction Layer

The network layer supports multiple transport protocols through a unified abstraction:

```
NetworkManager
    └── Transport Trait (abstraction)
        ├── TcpTransport (Bitcoin P2P compatible)
        └── IrohTransport (QUIC-based, optional)
```

### Transport Options

**TCP Transport** (Default): Fully implemented transport for Bitcoin P2P protocol compatibility using traditional TCP sockets. Maintains Bitcoin wire protocol format and is compatible with standard Bitcoin nodes.

**Iroh Transport** (Experimental): QUIC-based transport using Iroh for P2P networking with public key-based peer identity and NAT traversal support. Status: Skeleton complete, requires Iroh API integration for full functionality.

### Transport Selection

Configure transport via [node configuration](../node/configuration.md):

```toml
[network]
transport_preference = "tcp_only"  # or "iroh_only", "hybrid"
```

**Modes**: `tcp_only` (default, Bitcoin compatible), `iroh_only` (experimental), `hybrid` (both simultaneously)

The **protocol adapter** serializes between consensus-proof `NetworkMessage` types and transport-specific wire formats. The **message bridge** processes messages and generates responses. Default is TCP-only; enable Iroh via `iroh` feature flag.

## See Also

- [Protocol Architecture](architecture.md) - Protocol layer design
- [Message Formats](message-formats.md) - P2P message specifications
- [Protocol Overview](overview.md) - Protocol layer introduction
- [Node Configuration](../node/configuration.md) - Network and transport configuration
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations

