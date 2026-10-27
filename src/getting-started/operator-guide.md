# Operator guide

Install, run, and operate a BLVM node. For a five-minute regtest walkthrough see [Quick Start](quick-start.md). Read [Deployment posture](../security/deployment-posture.md) before exposing RPC on mainnet.

The `blvm` binary speaks Bitcoin Core JSON-RPC. Script history and Electrum `blockchain.scripthash.get_history` are the separate `blvm-wallet-index` process. Payment, vault, pool, and congestion methods are the separate `blvm-payment` process: `createpaymentrequest`, `createcovenantproof`, `getpaymentstate`, `listpayments`, `verifyonchainpayment`, `verifyonchainpaymentbytx`, `verifycovenantproof`, `createvault`, `unvault`, `withdrawfromvault`, `getvaultstate`, `createpool`, `joinpool`, `distributepool`, `getpoolstate`, `createbatch`, `addtobatch`, `getcongestion`, `getcongestionmetrics`, and `broadcastbatch`. The default node answers those names with method-not-found until that module is loaded. It is not in the default module set. Chain and mempool reads go through the node API. A `merchant_key` in the module `config.toml` signs a peer payment acknowledgement.

## Data directory

Chain data, the RPC cookie, and the node config you point at all live under one directory. Resolution order is the `--data-dir` flag, then `BLVM_DATA_DIR`, then `[storage].data_dir`, then `./data`.

```toml
[storage]
data_dir = "/var/lib/blvm"
```

```bash
blvm --data-dir /var/lib/blvm --network mainnet
```

Mainnet RPC listens on `127.0.0.1:8332` unless `--rpc-addr` is set. Regtest uses `127.0.0.1:18443`, testnet `127.0.0.1:18332`, signet `127.0.0.1:38332`, testnet4 `127.0.0.1:48332`.

## RPC authentication

Two credentials can be live at once. HTTP Basic from the cookie or from `[rpc_auth].password`, and Bearer tokens from `[rpc_auth]`.

### Cookie

When `[rpc_auth].password` is unset, startup writes `{data_dir}/.cookie`. The file is one line, `__cookie__:` plus 64 hex characters, mode `0600`. That pair is HTTP Basic, and it is an admin credential (`getblocktemplate`, `submitblock`, `stop`). Shutdown deletes the file this process wrote. The next start replaces it.

`bitcoin-cli` can use the same file if `-datadir` is this data directory and `-rpcport` is the BLVM port. Or pass the two halves yourself:

```bash
cookie=$(cat /var/lib/blvm/.cookie)
curl --user "$cookie" \
  --data-binary '{"jsonrpc":"1.0","id":"1","method":"getblockchaininfo","params":[]}' \
  -H 'content-type: text/plain;' \
  http://127.0.0.1:8332/
```

A configured password does not create `.cookie`. Set both fields together:

```toml
[rpc_auth]
username = "operator"
password = "replace-me"
```

Basic auth is cleartext on the wire. Keep it on loopback. See [Deployment posture](../security/deployment-posture.md).

### Bearer token

Tokens in `[rpc_auth].tokens`, `[rpc_auth].token_file` (one token per line), or `RPC_AUTH_TOKENS` (comma-separated) authenticate as `Authorization: Bearer <token>`. A token is read-only unless it is also listed in `admin_tokens`. Mining RPC needs an admin token. The cookie password is separate from this list.

```toml
[rpc_auth]
admin_tokens = ["mining"]
tokens = ["watch"]
```

```bash
curl -H "Authorization: Bearer watch" \
  --data-binary '{"jsonrpc":"1.0","id":"1","method":"getblockchaininfo","params":[]}' \
  -H 'content-type: text/plain;' \
  http://127.0.0.1:8332/
```

Which surface accepts which header: [RPC transport × authentication](../security/rpc-transport-auth-matrix.md).

## Sync status

`getblockchaininfo` field `initialblockdownload` is true while the connected chain is behind the stored header tip, and while no header height is stored. It is false once the connected height has caught that header tip, including a fresh chain whose only stored header is genesis.

`verificationprogress` is connected height divided by the stored header tip while the chain has not passed that tip. It is `1.0` when both heights are zero. It is `0.0` when no header height is stored.

This flag does not use a tip-age window. Clients that wait for `initialblockdownload` to become false are waiting for headers and blocks to meet, not for a clock.

Script checking stays on unless `assume_valid_hash` is set. The height field alone does not skip scripts.

## Wallet index

`blvm-wallet-index` is a module process with its own database. On `NewBlock` it stores each output as txid, vout, value, script, and height, and it records a spend when that prevout is already in its database. On `BlockDisconnected` it deletes rows at that height and above. It does not open the node chain database.

`getscripthistory` takes one script hex string and returns the outputs that created it. Txids use the same reversed hex as other node RPC hashes. Load the module binary the same way as the other modules (`loadmodule`, or a `[modules]` pin once it is published). `getaddressinfo` stays on the node.

Electrum protocol binds only when the module config sets `listen`. That file is `{module data dir}/config.toml`:

```toml
listen = "127.0.0.1:50001"
```

The methods on that port are `server.version`, `server.ping`, `server.banner`, `blockchain.scripthash.get_history`, and `blockchain.scripthash.subscribe`. Subscribe returns null when the script has no rows, and otherwise the status hash of `tx_hash:height:` for each history row. A later block or disconnect pushes that method again with the new status. The history entry for a script includes the transaction that created it and the transaction that spent it. This port does not serve block headers or mempool. The node RPC port is not an Electrum port.

## Initial block download (IBD)

Mainnet sync is parallel IBD: fetch bodies, apply through the UTXO engine, optionally checkpoint. **Timestamp BPS** (first–last `IBD:` print) is the published clock.

- Downloading the chain: [IBD UTXO engine](../node/ibd-engine.md) — [scoring clock](../node/ibd-engine.md#scoring-clock), [download](../node/ibd-engine.md#sync-tuning-guide)
- Serving blocks to peers in IBD: [IBD Bandwidth Protection](../node/ibd-protection.md)
- Parallel IBD rates: [Performance](../node/performance.md#parallel-initial-block-download-ibd)
