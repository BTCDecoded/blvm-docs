# Protocol Layer Architecture

The protocol layer (`blvm-protocol`) provides Bitcoin protocol abstraction that enables multiple Bitcoin variants and protocol evolution.

## Architecture Position

This crate sits at **stack layer 3** of the six-layer Bitcoin Commons architecture (technology stack):

```
1. Orange Paper (mathematical foundation)
2. blvm-consensus (pure math implementation)
3. blvm-protocol (Bitcoin abstraction) ← THIS CRATE
4. blvm-node (full node implementation)
5. blvm-sdk (developer toolkit)
6. blvm-commons (governance enforcement)
```

## Purpose

The blvm-protocol sits between the pure mathematical consensus rules (blvm-consensus) and the full Bitcoin implementation (blvm-node). It provides:

### Protocol Abstraction
- **Multiple Variants**: Support for mainnet, testnet, and regtest
- **Network Parameters**: Magic bytes, ports, genesis blocks, difficulty targets
- **Feature Flags**: SegWit, Taproot, RBF, and other protocol features
- **Validation Rules**: Protocol-specific size limits and validation logic

### Protocol Evolution
- **Network variants**: Mainnet, testnet, and regtest share the same consensus surface with different parameters (see variants below).
- **Feature management**: Protocol features (SegWit, Taproot, RBF, and related flags) are toggled by the protocol engine and build configuration.
- **Wire and transport**: P2P message formats and Bitcoin-compatible peer behavior live in **blvm-protocol**; the reference node delivers them over [transports](../node/transport-abstraction.md) (TCP by default; optional QUIC-based paths where features enable them). Treat **encrypted Bitcoin P2P (BIP324)** and other transport experiments as **build- and release-specific**—see **`blvm-protocol`** and **`blvm-node`** features and release notes rather than assuming one global default.
- **Breaking changes**: Tracked per crate semver and release notes.

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

For more details, see the [blvm-protocol README](https://github.com/BTCDecoded/blvm-protocol/blob/main/README.md).

## See Also

- [Protocol Overview](overview.md) - Protocol layer introduction
- [Network Protocol](network-protocol.md) - Transport and protocol details
- [Message Formats](message-formats.md) - P2P message specifications
- [Consensus Architecture](../consensus/architecture.md) - Underlying consensus layer
- [Node Configuration](../node/configuration.md) - Protocol variant configuration

