# Quick Start

Tutorial: install the binary, run a **regtest** node, query RPC, and mine one block. About five minutes. For mainnet, use [Mainnet initial sync](mainnet-sync.md) instead of the steps below.

**Prerequisites:** [Installation](installation.md) completed (`blvm` on your `PATH`).

## 1. Verify the binary

```bash
blvm --version
blvm --help
```

You should see a version string and help text (no “command not found”).

## 2. Start a regtest node

Use a dedicated data directory so this tutorial does not mix with other networks:

```bash
blvm --network regtest -d ~/.local/share/blvm-quickstart --verbose
```

In the first log lines, confirm:

- `Network: Regtest` (or equivalent)
- RPC listening on **`127.0.0.1:18332`** (default for testnet/regtest)

Leave this process running, or run it in another terminal for the RPC steps below.

## 3. Check chain state

Regtest uses RPC port **18332** (not mainnet 8332):

```bash
curl -s -X POST http://127.0.0.1:18332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

Expected: `"chain":"regtest"` and `"blocks":0` at genesis.

## 4. Mine one block (regtest)

`generatetoaddress` is supported on **regtest** when the node has a protocol engine wired (normal `blvm start`):

```bash
curl -s -X POST http://127.0.0.1:18332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"generatetoaddress","params":[1,"bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"],"id":2}'
```

Expected: JSON result with an array of one block hash (hex).

## 5. Confirm the new height

Run `getblockchaininfo` again (step 3). Expected: `"blocks":1` (or higher if you mined more).

You now have a running regtest node that processed at least one block.

## Next steps

- **Regtest with config file and peers:** [First Node Setup (regtest)](first-node.md)
- **Mainnet:** [Mainnet initial sync](mainnet-sync.md) and [Deployment posture](../security/deployment-posture.md)
- **Core datadir import:** [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir)
- **Build a module:** [Building your first module](first-module.md)
- **RPC details:** [RPC API Reference](../node/rpc-api.md)
- **Configuration:** [Node Configuration](../node/configuration.md)
