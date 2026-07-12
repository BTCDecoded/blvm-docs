# Network Protocol

The protocol layer abstracts Bitcoin's P2P network protocol, supporting multiple network variants. See [Protocol Overview](overview.md) for details.

## Protocol Abstraction

The blvm-protocol abstracts P2P message formats (standard Bitcoin wire protocol), connection management, peer discovery, block synchronization, and transaction relay. See [Protocol overview](overview.md) for stack position and components.

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

For implementation details, see the [blvm-protocol README](https://github.com/BTCDecoded/blvm-protocol/blob/main/README.md).

## Transport Abstraction Layer

The network layer supports multiple transport protocols through one abstraction (see [Transport Abstraction](../node/transport-abstraction.md)):

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

Configure transport via **`blvm.toml`** (top-level `NodeConfig` keys: there is **no** `[network]` table). See [Node configuration](../node/configuration.md).

```toml
transport_preference = "tcponly" # file: tcponly | irohonly | quinnonly | hybrid | all
```

**CLI / ENV** (e.g. `BLVM_NODE_TRANSPORT`) still accept human-readable forms like `tcp_only`, `iroh_only`, `hybrid`.

The **protocol adapter** serializes between blvm-consensus `NetworkMessage` types and transport-specific wire formats. The **message bridge** processes messages and generates responses. Default is TCP-only; enable Iroh via `iroh` feature flag.

## Bitcoin wire and framing (blvm-protocol)

**blvm-protocol** owns Bitcoin **P2P message** framing (message type, length, payload, checksum) and related helpers. For TCP, entry points such as **[node_tcp](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/node_tcp.rs)** tie that logic to the node’s socket path. Exact layering may evolve, treat **`blvm-protocol` `src/`** as the source of truth rather than this summary.

### Wire envelope

| Field | Size | Role |
|-------|------|------|
| Magic | 4 bytes | Separates mainnet / testnet / regtest on the wire |
| Command | 12 bytes | NUL-padded ASCII (`version`, `inv`, `block`, …) |
| Length | 4 bytes | Payload size (LE uint32) |
| Checksum | 4 bytes | Integrity check on payload |
| Payload | variable | Serialized per command |

Implementation: [blvm-protocol wire layer](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/wire/mod.rs).

### Protocol magic and ports

| Variant | Magic (hex) | Default P2P | Default RPC (`blvm`) |
|---------|-------------|-------------|----------------------|
| Mainnet | `f9beb4d9` | 8333 | 8332 |
| Testnet | `0b110907` | 18333 | 18332 |
| Regtest | `fabfb5da` | 18444 | 18443 |

Each variant also defines genesis hash, difficulty rules, halving interval, and feature activation heights. See [Protocol overview: Network parameters](overview.md#network-parameters).

### Common message types

| Category | Commands | Purpose |
|----------|----------|---------|
| Handshake | `version`, `verack` | Capability negotiation |
| Inventory | `inv`, `getdata`, `notfound` | Announce and fetch blocks/txs |
| Sync | `getheaders`, `headers`, `getblocks` | Header chain download |
| Relay | `tx`, `block`, `mempool`, `feefilter` | Transaction and block propagation |
| Keepalive | `ping`, `pong` | Connection health |

Extensions (compact blocks, UTXO commitments, governance) add commands documented in [Protocol overview: Network messages](overview.md#network-messages).

For detailed protocol specifications, see the [blvm-protocol README](https://github.com/BTCDecoded/blvm-protocol/blob/main/README.md).

## See Also

- [Protocol Overview](overview.md) - Protocol layer introduction
- [Node Configuration](../node/configuration.md) - Network and transport configuration
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations

