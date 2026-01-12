# Message Formats

The protocol layer defines message formats for Bitcoin P2P protocol communication.

## Protocol Variants

Each protocol variant (mainnet, testnet, regtest) has specific message formats and network parameters:

- **Magic Bytes**: Unique identifier for each network variant
- **Message Headers**: Standard Bitcoin message header format
- **Message Types**: `version`, `verack`, `inv`, `getdata`, `tx`, `block`, etc.

## Network Parameters

Protocol-specific parameters include:

- Default ports (mainnet: 8333, testnet: 18333, regtest: 18444)
- Genesis block hashes
- Difficulty adjustment intervals
- Block size limits
- Feature activation heights

For detailed protocol specifications, see the [blvm-protocol README](../../modules/blvm-protocol/README.md).

## See Also

- [Protocol Architecture](architecture.md) - Protocol layer design
- [Network Protocol](network-protocol.md) - Transport and message handling
- [Protocol Overview](overview.md) - Protocol layer introduction
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations

