# First Node Setup

Complete guide for setting up and configuring your first BLVM node.

## Step-by-Step Setup

### Step 1: Create Configuration Directory

```bash
mkdir -p ~/.config/blvm
cd ~/.config/blvm
```

### Step 2: Create Basic Configuration

Create a configuration file `blvm.toml`:

```toml
# Regtest for safe development
listen_addr = "127.0.0.1:18444"
protocol_version = "Regtest"

[storage]
data_dir = "~/.local/share/blvm"
database_backend = "auto"  # Selects by build features: RocksDB when rocksdb enabled, then TidesDB, Redb, Sled

[logging]
level = "info"  # info, debug, trace, warn, error
```

**RPC address** is set via `--rpc-addr` (default `127.0.0.1:18332` for regtest) or `BLVM_RPC_ADDR`. Not in config file.

### Step 3: Start the Node

```bash
blvm --config ~/.config/blvm/blvm.toml
# Or: blvm -n regtest -d ~/.local/share/blvm
```

**Expected Output:**
```
[INFO] Starting BLVM node
[INFO] Network: regtest
[INFO] Data directory: ~/.local/share/blvm
[INFO] RPC server listening on 127.0.0.1:18332
[INFO] Connecting to network...
[INFO] Connected to 0 peers
```

### Step 4: Verify Node is Running

In another terminal, check the node status:

```bash
curl -X POST http://localhost:18332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "chain": "regtest",
    "blocks": 0,
    "headers": 0,
    "bestblockhash": "...",
    "difficulty": 4.656542373906925e-10,
    "mediantime": 1231006505,
    "verificationprogress": 1.0,
    "chainwork": "0000000000000000000000000000000000000000000000000000000000000001",
    "pruned": false,
    "initialblockdownload": false
  },
  "id": 1
}
```

## Configuration Examples

### Development Node (Regtest)

```toml
listen_addr = "127.0.0.1:18444"
protocol_version = "Regtest"

[storage]
data_dir = "~/.local/share/blvm"
database_backend = "auto"

[rbf]
mode = "standard"  # Standard RBF for development

[mempool]
max_mempool_mb = 100
min_relay_fee_rate = 1
```

Start with: `blvm -n regtest -d ~/.local/share/blvm` (RPC defaults to `127.0.0.1:18332`)

### Testnet Node

```toml
listen_addr = "127.0.0.1:18333"
protocol_version = "Testnet3"

[storage]
data_dir = "~/.local/share/blvm-testnet"
database_backend = "redb"

[rbf]
mode = "standard"

[mempool]
max_mempool_mb = 300
min_relay_fee_rate = 1
eviction_strategy = "lowest_fee_rate"
```

Start with: `blvm -n testnet -d ~/.local/share/blvm-testnet -r 127.0.0.1:18332`

### Production Mainnet Node

```toml
listen_addr = "0.0.0.0:8333"
protocol_version = "BitcoinV1"

[storage]
data_dir = "/var/lib/blvm"
database_backend = "redb"

[storage.cache]
# Example values; canonical defaults in [Configuration Reference](../reference/configuration-reference.md)
block_cache_mb = 200
utxo_cache_mb = 100
header_cache_mb = 20

[rbf]
mode = "standard"

[mempool]
max_mempool_mb = 300
max_mempool_txs = 100000
min_relay_fee_rate = 1
eviction_strategy = "lowest_fee_rate"
max_ancestor_count = 25
max_descendant_count = 25
```

Start with: `blvm -n mainnet -d /var/lib/blvm -r 127.0.0.1:8332`. Use `[rpc_auth]` and `RPC_AUTH_TOKENS` for production.

See [Node Configuration](../node/configuration.md) for complete configuration options.

## Storage

The node stores blockchain data (blocks, UTXO set, chain state, and indexes) in the configured data directory. See [Storage Backends](../node/storage-backends.md) for configuration options.

## Network Connection

The node automatically discovers peers, connects to the network, syncs blockchain state, and relays transactions and blocks.

## RPC Interface

Once running, interact with the node via JSON-RPC:

```bash
# Get blockchain info (mainnet uses port 8332, testnet/regtest use 18332)
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

