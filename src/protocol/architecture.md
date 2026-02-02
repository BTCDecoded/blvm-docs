# Protocol Layer Architecture

The protocol layer (`blvm-protocol`) provides Bitcoin protocol abstraction that enables multiple Bitcoin variants and protocol evolution.

## Architecture Position

This is **Tier 3** of the 5-tier Bitcoin Commons architecture (BLVM technology stack):

```
1. Orange Paper (mathematical foundation)
2. blvm-consensus (pure math implementation)
3. blvm-protocol (Bitcoin abstraction) ← THIS CRATE
4. blvm-node (full node implementation)
5. blvm-sdk (developer toolkit)
```

## Purpose

The blvm-protocol sits between the pure mathematical consensus rules (blvm-consensus) and the full Bitcoin implementation (blvm-node). It provides:

### Protocol Abstraction
- **Multiple Variants**: Support for mainnet, testnet, and regtest
- **Network Parameters**: Magic bytes, ports, genesis blocks, difficulty targets
- **Feature Flags**: SegWit, Taproot, RBF, and other protocol features
- **Validation Rules**: Protocol-specific size limits and validation logic

### Protocol Evolution
- **Version Support**: Bitcoin V1, V2 (planned), and experimental variants
- **Feature Management**: Enable/disable features based on protocol version
- **Breaking Changes**: Track and manage protocol evolution

## Core Components

### Protocol Variants
- **BitcoinV1**: Production Bitcoin mainnet
- **Testnet3**: Bitcoin test network
- **Regtest**: Regression testing network

### Network Parameters
- **Magic Bytes**: P2P protocol identification
- **Ports**: Default network ports
- **Genesis Blocks**: Network-specific genesis blocks
- **Difficulty**: Proof-of-work targets
- **Halving**: Block subsidy intervals

For more details, see the [blvm-protocol README](../../blvm-protocol/README.md).

## See Also

- [Protocol Overview](overview.md) - Protocol layer introduction
- [Network Protocol](network-protocol.md) - Transport and protocol details
- [Message Formats](message-formats.md) - P2P message specifications
- [Consensus Architecture](../consensus/architecture.md) - Underlying consensus layer
- [Node Configuration](../node/configuration.md) - Protocol variant configuration

