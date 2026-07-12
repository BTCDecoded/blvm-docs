# Network Protocol

Bitcoin **P2P wire format** and framing in **blvm-protocol**. For the protocol engine, variants, message catalog, service flags, and BIPs: [Protocol Overview](overview.md). For transports (TCP, Quinn, Iroh), `transport_preference`, and the `NetworkManager`: [Transport Abstraction](../node/transport-abstraction.md). For operator bind addresses and CLI defaults: [Node Configuration](../node/configuration.md).

## Bitcoin wire and framing (blvm-protocol)

**blvm-protocol** owns Bitcoin **P2P message** framing (message type, length, payload, checksum) and related helpers. For TCP, entry points such as **[node_tcp](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/node_tcp.rs)** tie that logic to the node’s socket path. Treat **`blvm-protocol` `src/`** as the source of truth rather than this summary.

### Wire envelope

| Field | Size | Role |
|-------|------|------|
| Magic | 4 bytes | Separates mainnet / testnet / regtest on the wire |
| Command | 12 bytes | NUL-padded ASCII (`version`, `inv`, `block`, …) |
| Length | 4 bytes | Payload size (LE uint32) |
| Checksum | 4 bytes | Integrity check on payload |
| Payload | variable | Serialized per command |

Implementation: [blvm-protocol wire layer](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/wire/mod.rs).

### Network identifiers on the wire

Magic bytes and default P2P/RPC ports per variant: [Protocol overview: Protocol variants](overview.md#protocol-variants).

### Message taxonomy

Handshake, inventory, sync, relay, keepalive, and Commons extension commands: [Protocol overview: Network messages](overview.md#network-messages).

## See Also

- [Protocol Overview](overview.md) - Protocol layer introduction
- [Transport Abstraction](../node/transport-abstraction.md) - TCP, Quinn, and Iroh transports
- [Node Configuration](../node/configuration.md) - Network and transport configuration
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations
