# Message Formats

Bitcoin P2P messages share a common wire envelope; payload layout depends on command type and network variant.

## Wire envelope

| Field | Size | Role |
|-------|------|------|
| Magic | 4 bytes | Separates mainnet / testnet / regtest on the wire |
| Command | 12 bytes | NUL-padded ASCII (`version`, `inv`, `block`, …) |
| Length | 4 bytes | Payload size (LE uint32) |
| Checksum | 4 bytes | Integrity check on payload |
| Payload | variable | Serialized per command |

Implementation: [`blvm-protocol` wire layer](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/wire/mod.rs).

## Protocol variants

| Variant | Magic (hex) | Default P2P | Default RPC (`blvm`) |
|---------|-------------|-------------|----------------------|
| Mainnet | `f9beb4d9` | 8333 | 8332 |
| Testnet | `0b110907` | 18333 | 18332 |
| Regtest | `fabfb5da` | 18444 | 18443 |

Each variant also defines genesis hash, difficulty rules, halving interval, and feature activation heights. See [Protocol overview — Network parameters](overview.md#network-parameters).

## Common message types

| Category | Commands | Purpose |
|----------|----------|---------|
| Handshake | `version`, `verack` | Capability negotiation |
| Inventory | `inv`, `getdata`, `notfound` | Announce and fetch blocks/txs |
| Sync | `getheaders`, `headers`, `getblocks` | Header chain download |
| Relay | `tx`, `block`, `mempool`, `feefilter` | Transaction and block propagation |
| Keepalive | `ping`, `pong` | Connection health |

Extensions (compact blocks, UTXO commitments, governance) add commands documented in [Protocol overview](overview.md#network-messages).

For detailed protocol specifications, see the [blvm-protocol README](https://github.com/BTCDecoded/blvm-protocol/blob/main/README.md).

## See Also

- [Protocol Architecture](architecture.md) - Protocol layer design
- [Network Protocol](network-protocol.md) - Transport and message handling
- [Protocol Overview](overview.md) - Protocol layer introduction
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations
