# First Node Setup (regtest)

**This guide is regtest-only from top to bottom** — local chain, no public seeds, default RPC `127.0.0.1:18332`. You are not syncing mainnet here.

Optional later: [Configuration examples](#configuration-examples) include testnet and mainnet. Ignore those until you intentionally switch networks.

---

## Regtest: step-by-step

### Step 1: Create configuration directory

```bash
mkdir -p ~/.config/blvm
cd ~/.config/blvm
```

### Step 2: Create `blvm.toml` (regtest)

Create `~/.config/blvm/blvm.toml`:

```toml
# --- regtest (local dev) ---
transport_preference = "tcponly"
# BLVM P2P listen — use a port other than 18444 if Bitcoin Core -regtest runs here (Core uses 18444).
listen_addr = "127.0.0.1:18445"
protocol_version = "Regtest"

[storage]
data_dir = "~/.local/share/blvm"
database_backend = "auto"

[logging]
level = "info"
```

- **`transport_preference`** is required. If TOML parse fails, the node never applies `protocol_version = "Regtest"` — fix the file before continuing.
- **P2P port:** `18444` is Bitcoin Core’s default regtest listen. Give BLVM a different port (e.g. `18445`) whenever Core and BLVM run on the same host; point `persistent_peers` at Core’s `127.0.0.1:18444` when you want IBD from Core.
- **RPC** is not in this file: use defaults (`127.0.0.1:18332`) or `--rpc-addr` / `BLVM_RPC_ADDR`.

### Step 2b: Validate the file

From any directory, using the same `blvm` binary you will run:

```bash
/path/to/blvm config validate --path ~/.config/blvm/blvm.toml
```

You should see **`Configuration file is valid`**. If not, fix the TOML; do not start sync until this passes.

### Step 3: Start the regtest node

Same binary as validate. Clear mainnet IBD env vars if your shell still has them from other work:

```bash
env -u BLVM_ASSUME_VALID_HEIGHT -u BLVM_ASSUMEVALID \
  /path/to/blvm --config ~/.config/blvm/blvm.toml --verbose
```

**Confirm regtest in the first log lines:**

- `Configuration loaded successfully from file`
- **`Network: Regtest`**
- `Data directory:` matches your `[storage].data_dir`

**No config file** (still regtest):

```bash
env -u BLVM_ASSUME_VALID_HEIGHT -u BLVM_ASSUMEVALID \
  /path/to/blvm -n regtest -d ~/.local/share/blvm --verbose
```

Example lines:

```
[INFO] blvm: Network: Regtest
[INFO] blvm: Data directory: /home/you/.local/share/blvm
[INFO] blvm_node::rpc: Starting TCP RPC server on 127.0.0.1:18332
```

**Peers on regtest:** there are no public DNS seeds. **`0 peers`** and “skipping DNS seed discovery” are normal. To sync blocks you need another regtest peer (e.g. second `blvm`, or Bitcoin Core `-regtest`) and `persistent_peers` / a local harness — that is still regtest, not mainnet.

### Step 4: Verify regtest RPC

In another terminal (regtest RPC port **18332**):

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

## Configuration examples (other networks)

The steps above are **regtest**. Below are copy-paste starting points if you leave regtest.

### Development node (regtest, extended)

```toml
transport_preference = "tcponly"
listen_addr = "127.0.0.1:18445"
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

Start with: `blvm -n regtest -d ~/.local/share/blvm` (RPC defaults to `127.0.0.1:18332`).

### Testnet node

```toml
transport_preference = "tcponly"
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

### Production mainnet node

```toml
transport_preference = "tcponly"
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

## Peers and sync (regtest vs public networks)

- **Regtest:** No wide-area peer discovery. You only get blocks from peers you configure (`persistent_peers`, local second node, or Core `-regtest`). Staying at height 0 with 0 peers is expected until you add that.
- **Mainnet / testnet:** DNS seeds and addr relay apply; IBD pulls from the public network.

## Regtest: how you get past genesis (`height > 0`)

You need **a peer that already has blocks**, or a **datadir that already contains** those blocks. A lone BLVM on regtest with no peers stays at genesis — that is not “missing a feature,” it is how regtest is defined (no public seeds).

**1. Bitcoin Core regtest (the usual way to create blocks)**

Run Core on default regtest P2P **`127.0.0.1:18444`**, mine some blocks, then run BLVM on a **different** local P2P port and peer **outbound** to Core. Example Core side:

```bash
bitcoind -regtest -daemon
bitcoin-cli -regtest createwallet w
ADDR=$(bitcoin-cli -regtest getnewaddress)
bitcoin-cli -regtest generatetoaddress 200 "$ADDR"
```

BLVM TOML (listen on `18445`, sync from Core on `18444`; matches `local/regtest-two-node-seed-bootstrap.toml`):

```toml
transport_preference = "tcponly"
listen_addr = "127.0.0.1:18445"
protocol_version = "Regtest"

persistent_peers = ["127.0.0.1:18444"]

[storage]
data_dir = "~/.local/share/blvm-regtest-from-core"
database_backend = "auto"

[ibd]
mode = "parallel"
preferred_peers = ["127.0.0.1:18444"]

[logging]
level = "info"
```

Start BLVM with that config (or pass `--listen-addr 127.0.0.1:18445` if your file is merged with other settings); IBD should pull blocks until it matches Core’s tip.

**2. Two BLVM nodes**

Works once the **seed** already has `height > 0` (from (1), or from copying a populated seed `data_dir`). A **follower** then syncs from the seed over `persistent_peers`. If both nodes start from an empty datadir, both stay at genesis — add blocks with (1) first, or reuse a filled datadir.

**3. Reuse a populated data directory**

Copy/sync the configured `[storage].data_dir` from a machine that already completed regtest sync for the same network.

**4. `submitblock` on a running BLVM node**

On a normal node (RPC server wired with `NetworkManager`), `submitblock` checks that the block’s `prev_block_hash` matches the **current tip**, then **queues the block for the same run-loop processing as P2P-received blocks**, so a valid next block can extend your local chain. You still have to **produce** that block (for example `getblocktemplate` plus a miner); BLVM does not offer Core’s `generatetoaddress` yet.

If `MiningRpc` is used without a network manager (some tests or minimal tooling), `submitblock` remains **validation-only** and does not advance the chain.

If you use the workspace **local harness** (`BitcoinCommons/local/regtest-two-blvm.sh`), `regtest-two-node-seed-bootstrap.toml` is wired for Core on **:18444** and seed P2P on **:18445**. After Core has blocks, run **`./local/regtest-two-blvm.sh start-seed-bootstrap`**, then **`start-follower`** (or **`start-both`** after the seed has height > 0) as documented in the script header.

## RPC interface (regtest)

Default listen in this guide: **`127.0.0.1:18332`**.

```bash
curl -s -X POST http://127.0.0.1:18332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

Mainnet uses port **8332** by default; do not use that for the regtest flow above.

See [RPC API Reference](../node/rpc-api.md) for the full API.

## See Also

- [Node Configuration](../node/configuration.md) - Complete configuration options
- [Node Operations](../node/operations.md) - Running and managing your node
- [RPC API Reference](../node/rpc-api.md) - Complete API documentation
- [Troubleshooting](../appendices/troubleshooting.md) - Common issues and solutions

## Security Considerations

⚠️ **Important**: This implementation is designed for pre-production testing and development. Additional hardening is required for production mainnet use. Use regtest or testnet for development, never expose RPC to untrusted networks, configure RPC authentication, and keep software updated.

## Troubleshooting

See [Troubleshooting](../appendices/troubleshooting.md) for common issues and solutions.

