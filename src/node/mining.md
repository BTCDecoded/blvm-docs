# Mining Integration

The reference node includes mining coordination functionality as part of the Bitcoin protocol.

## Mining Components

### Block Template Generation

Block templates are created from mempool transactions, selecting transactions based on fee priority, generating coinbase transactions, and calculating merkle roots.

### Mining Process

The mining process involves block template creation, nonce finding and proof-of-work, and block submission and validation.

## Mining Integration

The node provides a **Block Template API** for generating blocks for mining, **mining coordination** with mining hardware/software, and optional **Stratum V2 support** (feature-gated).

For implementation details, see the [bllvm-node README](../../modules/bllvm-node/README.md).

## See Also

- [Node Operations](operations.md) - Node operation and management
- [RPC API Reference](rpc-api.md) - Mining-related RPC methods (`getblocktemplate`, `submitblock`)
- [Node Configuration](configuration.md) - Mining configuration options
- [Protocol Specifications](../reference/protocol-specifications.md) - Stratum V2 and mining protocols

