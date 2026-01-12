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
[network]
protocol = "regtest"  # Start with regtest for safe testing
port = 18444          # Regtest default port

[storage]
data_dir = "~/.local/share/blvm"
backend = "auto"      # Auto-select best available backend

[rpc]
enabled = true
port = 18332         # Regtest RPC port
host = "127.0.0.1"   # Only listen on localhost

[logging]
level = "info"       # info, debug, trace, warn, error
```

### Step 3: Start the Node

```bash
blvm --config ~/.config/blvm/blvm.toml
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
[network]
protocol = "regtest"
port = 18444

[storage]
data_dir = "~/.local/share/blvm"
backend = "auto"

[rpc]
enabled = true
port = 18332
host = "127.0.0.1"

[rbf]
mode = "standard"  # Standard RBF for development

[mempool]
max_mempool_mb = 100
min_relay_fee_rate = 1
```

### Testnet Node

```toml
[network]
protocol = "testnet"
port = 18333

[storage]
data_dir = "~/.local/share/blvm-testnet"
backend = "redb"

[rpc]
enabled = true
port = 18332
host = "127.0.0.1"

[rbf]
mode = "standard"

[mempool]
max_mempool_mb = 300
min_relay_fee_rate = 1
eviction_strategy = "lowest_fee_rate"
```

### Production Mainnet Node

```toml
[network]
protocol = "mainnet"
port = 8333

[storage]
data_dir = "/var/lib/blvm"
backend = "redb"

[storage.cache]
block_cache_mb = 200
utxo_cache_mb = 100
header_cache_mb = 20

[rpc]
enabled = true
port = 8332
host = "127.0.0.1"
# Enable authentication for production
# auth_required = true

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

See [Node Configuration](../node/configuration.md) for complete configuration options.

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

