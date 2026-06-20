# First Node Setup

Config-file walkthrough: create `~/.config/blvm/blvm.toml`, validate it, start the node, and confirm RPC. For a five-minute regtest tutorial, use [Quick Start](quick-start.md) instead.

**Mainnet first sync:** after your config is in place, follow [Mainnet initial sync](mainnet-sync.md) (bundled IBD example, pruning, and sync expectations). Do not rely on bare `blvm --network mainnet` alone for initial block download.

---

## Choose a network

| Network | `protocol_version` | Default P2P | Default RPC | Next step |
|---------|---------------------|-------------|-------------|-----------|
| **Mainnet** | `BitcoinV1` | `0.0.0.0:8333` | `127.0.0.1:8332` | [Mainnet initial sync](mainnet-sync.md) |
| **Testnet** | `Testnet3` | `0.0.0.0:18333` | `127.0.0.1:18332` | Public DNS seeds; separate `data_dir` |
| **Regtest** | `Regtest` | `0.0.0.0:18444` | `127.0.0.1:18443` | [Quick Start](quick-start.md) |

Use a **separate `[storage].data_dir` per network** so chain state never mixes.

---

## Step 1: Create configuration directory

```bash
mkdir -p ~/.config/blvm
```

## Step 2: Create `blvm.toml`

Example for **mainnet** (`~/.config/blvm/blvm.toml`):

```toml
transport_preference = "tcponly"
listen_addr = "0.0.0.0:8333"
protocol_version = "BitcoinV1"

[storage]
data_dir = "~/.local/share/blvm-mainnet"
database_backend = "auto"

[logging]
level = "info"
```

- **`transport_preference`** is required in TOML (no serde default when loading a file). If parse fails, the node never applies `protocol_version` — fix the file before continuing.
- **RPC bind** is not set in this minimal file: defaults to `127.0.0.1:8332` on mainnet when `--network` / `protocol_version` resolve to mainnet. Override with `--rpc-addr` / `BLVM_RPC_ADDR`. The optional **`[rpc]`** table is for limits only (not bind address) — see [Node Configuration](../node/configuration.md).
- **Production:** configure `[rpc_auth]` before exposing RPC beyond loopback. See [Deployment posture](../security/deployment-posture.md) and [RPC transport × authentication](../security/rpc-transport-auth-matrix.md).

### Step 2b: Validate the file

```bash
blvm config validate ~/.config/blvm/blvm.toml
```

Expected: **`Configuration file is valid:`** (with the path). Do not start sync until this passes.

## Step 3: Start the node

Clear stale IBD env vars if your shell still has them from other work:

```bash
env -u BLVM_ASSUME_VALID_HEIGHT \
  blvm --config ~/.config/blvm/blvm.toml --verbose
```

**Confirm in the first log lines:**

- `Configuration loaded successfully from file`
- **`Network: Mainnet`** (or your chosen network)
- `Data directory:` matches `[storage].data_dir`

For **first mainnet sync**, use the bundled script from a [release tarball](installation.md) or the `blvm` repo root — see [Mainnet initial sync](mainnet-sync.md):

```bash
./scripts/start-ibd-mainnet.sh
```

## Step 4: Verify RPC

Mainnet default RPC port **8332**; testnet **18332**; regtest **18443** (Core-aligned):

```bash
curl -s -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

During IBD, expect `"initialblockdownload": true` and rising `"blocks"`. After sync, `"initialblockdownload"` becomes `false`.

See [RPC API Reference](../node/rpc-api.md) for authentication and the full method list.

---

## Configuration examples (other networks)

### Testnet

Example **`~/.config/blvm/blvm-testnet.toml`**:

```toml
transport_preference = "tcponly"
listen_addr = "0.0.0.0:18333"
protocol_version = "Testnet3"

[storage]
data_dir = "~/.local/share/blvm-testnet"
database_backend = "auto"

[mempool]
max_mempool_mb = 300
min_relay_fee_rate = 1
```

Start: `blvm --config ~/.config/blvm/blvm-testnet.toml --verbose`

### Regtest (local dev)

```toml
transport_preference = "tcponly"
listen_addr = "127.0.0.1:18445"   # default P2P is 18444; pick another if Core/bitcoind uses 18444
protocol_version = "Regtest"

[storage]
data_dir = "~/.local/share/blvm-regtest"
database_backend = "auto"

[rpc_auth]
admin_tokens = ["dev"]
```

Regtest has **no public seeds** — `0 peers` is normal until you add `persistent_peers` or mine locally. See [Quick Start](quick-start.md) for a minimal regtest flow with `generatetoaddress`.

### Production mainnet (extended)

Start from [Mainnet initial sync](mainnet-sync.md) and the release `blvm-mainnet-ibd.toml.example`. Custom TOML additions:

```toml
[storage.cache]
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
```

See [Node Configuration](../node/configuration.md) and [Configuration Reference](../reference/configuration-reference.md) for all keys and defaults.

---

## Storage

The node stores blocks, UTXO set, chain state, and indexes under `[storage].data_dir`. See [Storage Backends](../node/storage-backends.md).

## Peers and sync

- **Mainnet / testnet:** DNS seeds and addr relay; IBD pulls from the public network.
- **Regtest:** peer only nodes you configure (`persistent_peers`, local second node, or a regtest `bitcoind`). Height stays at genesis with no peers — expected until you add one.

## See also

- [Mainnet initial sync](mainnet-sync.md) — IBD script, expectations, resume
- [Node Configuration](../node/configuration.md) — complete options
- [Node Operations](../node/operations.md) — start/stop, backup, Core datadir import
- [RPC API Reference](../node/rpc-api.md)
- [Troubleshooting](../appendices/troubleshooting.md)
