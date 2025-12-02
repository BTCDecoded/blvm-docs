# First Node Setup

Complete guide for setting up and configuring your first BLVM node.

## Configuration

See [Node Configuration](../node/configuration.md) for complete configuration options.

### Basic Configuration

Create a configuration file `blvm.toml`:

```toml
[network]
protocol = "regtest"  # or "testnet" or "mainnet"

[storage]
data_dir = "/var/lib/blvm"

[rpc]
enabled = true
port = 8332
```

### Running with Configuration

```bash
blvm --config blvm.toml
```

## Storage

The node stores blockchain data (blocks, UTXO set, chain state, and indexes) in the configured data directory. See [Storage Backends](../node/configuration.md#storage-backends) for configuration options.

## Network Connection

The node automatically discovers peers, connects to the network, syncs blockchain state, and relays transactions and blocks.

## RPC Interface

Once running, interact with the node via JSON-RPC:

```bash
# Get blockchain info
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

See [RPC API Reference](../node/rpc-api.md) for complete API documentation.

## See Also

- [Node Configuration](../node/configuration.md) - Complete configuration options
- [Node Operations](../node/operations.md) - Running and managing your node
- [RPC API Reference](../node/rpc-api.md) - Complete API documentation
- [Troubleshooting](../appendices/troubleshooting.md) - Common issues and solutions

## Security Considerations

⚠️ **Important**: This implementation is designed for pre-production testing and development. Additional hardening is required for production mainnet use. Use regtest or testnet for development, never expose RPC to untrusted networks, configure RPC authentication, and keep software updated.

## Troubleshooting

See [Troubleshooting](../appendices/troubleshooting.md) for common issues and solutions.

