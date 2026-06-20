# Quick Start

Tutorial: install the binary, run a **regtest** node, query RPC, and mine one block. About five minutes. For mainnet, use [First Node Setup — Mainnet IBD](first-node.md#mainnet-initial-sync) instead of the steps below.

**Prerequisites:** [Installation](installation.md) completed (`blvm` on your `PATH`).

## 1. Verify the binary

```bash
blvm version
blvm --help
```

You should see a version string and help text (no “command not found”). Version is a **subcommand** (`blvm version`), not `blvm --version`.

## 2. Start a regtest node

Use a dedicated data directory and a minimal config so regtest mining RPCs work (`generatetoaddress` is **admin-only**):

```bash
mkdir -p ~/.local/share/blvm-quickstart
cat > ~/.local/share/blvm-quickstart/blvm.toml <<'EOF'
transport_preference = "tcponly"
protocol_version = "Regtest"

[storage]
data_dir = "~/.local/share/blvm-quickstart"

[rpc_auth]
admin_tokens = ["quickstart"]
EOF

blvm --config ~/.local/share/blvm-quickstart/blvm.toml --verbose
```

In the first log lines, confirm:

- `Network: Regtest` (or equivalent)
- RPC listening on **`127.0.0.1:18443`** (regtest default; testnet uses **18332**)

Leave this process running. On a **fresh datadir**, wait until logs show **`Component startup complete`** or **`NodeStartupCompleted`** (~10–15 seconds) before mining in step 4 — RPC listens earlier, but `generatetoaddress` needs an initialized chain tip.

## 3. Check chain state

Regtest uses RPC port **18443** (Core-aligned; mainnet **8332**, testnet **18332**):

```bash
curl -s -X POST http://127.0.0.1:18443 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

Expected at genesis: `"chain":"regtest"` and `"blocks":0`.

## 4. Mine one block (regtest)

`generatetoaddress` requires an **admin** Bearer token (listed in `[rpc_auth].admin_tokens`):

```bash
curl -s -X POST http://127.0.0.1:18443 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer quickstart" \
  -d '{"jsonrpc":"2.0","method":"generatetoaddress","params":[1,"bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"],"id":2}'
```

Expected: JSON result with an array of one block hash (hex). Without the Bearer header you get HTTP **403** (`requires admin privileges`).

## 5. Confirm the new height

Run `getblockchaininfo` again (step 3). Expected: `"blocks":1` (or higher if you mined more).

You now have a running regtest node that processed at least one block.

## Next steps

- **Config file and mainnet/testnet:** [First Node Setup](first-node.md)
- **Mainnet:** [First Node Setup — Mainnet IBD](first-node.md#mainnet-initial-sync) and [Deployment posture](../security/deployment-posture.md)
- **Core datadir import:** [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir)
- **Build a module:** [Building your first module](first-module.md)
- **RPC details:** [RPC API Reference](../node/rpc-api.md)
- **Configuration:** [Node Configuration](../node/configuration.md)
