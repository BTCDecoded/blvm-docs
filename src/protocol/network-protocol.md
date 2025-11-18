# Network Protocol

The protocol layer abstracts Bitcoin's P2P network protocol, enabling support for multiple network variants.

## Protocol Abstraction

The bllvm-protocol provides abstraction for:

- **P2P Message Formats**: Standard Bitcoin wire protocol messages
- **Connection Management**: Network connection handling
- **Peer Discovery**: Finding and connecting to peers
- **Block Synchronization**: Downloading and validating blocks
- **Transaction Relay**: Broadcasting transactions

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

**TCP Transport** (Default):
- Fully implemented transport for Bitcoin P2P protocol compatibility
- Uses traditional TCP sockets
- Maintains Bitcoin wire protocol format
- Compatible with standard Bitcoin nodes

**Iroh Transport** (Experimental):
- QUIC-based transport using Iroh for P2P networking
- Public key-based peer identity
- NAT traversal support
- **Status**: Skeleton complete, requires Iroh API integration for full functionality

### Transport Selection

Transport preference can be configured via `NodeConfig`:

```json
{
  "network": {
    "transport_preference": "tcp_only"  // or "iroh_only", "hybrid"
  }
}
```

**Transport Modes:**
- `tcp_only`: Use only TCP transport (default, Bitcoin compatible)
- `iroh_only`: Use only Iroh transport (experimental)
- `hybrid`: Use both TCP and Iroh simultaneously

### Protocol Adapter

The protocol adapter handles message serialization between:
- Consensus-proof `NetworkMessage` types
- Transport-specific wire formats (TCP Bitcoin P2P vs Iroh message format)

### Message Bridge

The message bridge connects consensus-proof message processing with the transport layer:
- Converts messages to/from transport formats
- Processes incoming messages
- Generates responses

### Feature Flags

- **Default**: TCP-only (Bitcoin compatible)
- **`iroh` feature**: Enable Iroh transport support

