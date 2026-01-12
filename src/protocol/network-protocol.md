# Network Protocol

The protocol layer abstracts Bitcoin's P2P network protocol, supporting multiple network variants. See [Protocol Overview](overview.md) for details.

## Protocol Abstraction

The blvm-protocol abstracts P2P message formats (standard Bitcoin wire protocol), connection management, peer discovery, block synchronization, and transaction relay. See [Protocol Architecture](architecture.md) for details.

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

For implementation details, see the [blvm-protocol README](../../modules/blvm-protocol/README.md).

## Transport Abstraction Layer

The network layer uses multiple transport protocols through a unified abstraction (see [Transport Abstraction](../node/transport-abstraction.md)):

```
NetworkManager
    └── Transport Trait (abstraction)
        ├── TcpTransport (Bitcoin P2P compatible)
        └── IrohTransport (QUIC-based, optional)
```

### Transport Options

**TCP Transport** (Default): Bitcoin P2P protocol compatibility using traditional TCP sockets. Maintains Bitcoin wire protocol format and is compatible with standard Bitcoin nodes. See [Transport Abstraction](../node/transport-abstraction.md#tcp-transport).

**Iroh Transport**: QUIC-based transport using Iroh for P2P networking with public key-based peer identity and NAT traversal support. See [Transport Abstraction](../node/transport-abstraction.md#iroh-transport).

### Transport Selection

Configure transport via [node configuration](../node/configuration.md):

```toml
[network]
transport_preference = "tcp_only"  # or "iroh_only", "hybrid"
```

**Modes**: `tcp_only` (default, Bitcoin compatible), `iroh_only` (experimental), `hybrid` (both simultaneously)

The **protocol adapter** serializes between blvm-consensus `NetworkMessage` types and transport-specific wire formats. The **message bridge** processes messages and generates responses. Default is TCP-only; enable Iroh via `iroh` feature flag.

## See Also

- [Protocol Architecture](architecture.md) - Protocol layer design
- [Message Formats](message-formats.md) - P2P message specifications
- [Protocol Overview](overview.md) - Protocol layer introduction
- [Node Configuration](../node/configuration.md) - Network and transport configuration
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations

