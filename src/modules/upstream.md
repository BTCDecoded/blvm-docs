# Upstream connectors (`blvm-upstream`)

`blvm-upstream` fetches tip and fee data from outside the node: mempool.space, Esplora, and a bitcoind JSON-RPC endpoint. It serves that data to other modules through the `blvm.upstream.v1` module API. [blvm-fees](fees.md) is the consumer in this repository set.

It is **not** a default module pin, and it is not in `registry/modules.json`. Source: [BTCDecoded/blvm-upstream](https://github.com/BTCDecoded/blvm-upstream). Crate: `blvm-upstream` on crates.io.

## Network access

The module has no direct socket. HTTP goes through the node's outbound broker (`module-http`). It is a `blvm-node` default feature, but the `blvm` default and release feature sets do not enable it; build `blvm` with `--features blvm-node/module-http`. The operator allow-list controls what it may reach:

```toml
[module_network.blvm-upstream]
http_allow = ["https://mempool.space", "https://blockstream.info"]
```

The module's own tests use a local mock and do not call mempool.space or Blockstream.

## Manifest

`module.toml` declares the capabilities `http_client`, `subscribe_events`, and `register_module_api`, plus `provides_apis = ["blvm.upstream.v1"]`.

## Configuration

The module reads `<module data dir>/config.toml`. `poll_interval_secs` and `timeout_ms` can also be overridden by scalars in `[modules.blvm-upstream]` in the node config. The `sources` array stays in the module file. With no sources configured, the module has nothing to poll.

```toml
poll_interval_secs = 10   # default; must be at least 1
timeout_ms = 5000         # default; must be at least 1

[[sources]]
id = "mempool-space"
kind = "mempool-space"
base_url = "https://mempool.space"

[[sources]]
id = "blockstream"
kind = "esplora"
base_url = "https://blockstream.info"
# fallback_base_url = "https://..."

# [[sources]]
# id = "core"
# kind = "bitcoind-rpc"
# base_url = "http://127.0.0.1:8332"
# rpc_user = "..."
# rpc_password = "..."
```

`kind` must be `mempool-space`, `esplora`, or `bitcoind-rpc`. Each `id` must be unique. A `bitcoind-rpc` source asks for `estimatesmartfee`, `getmempoolinfo`, `getblockcount`, and `getbestblockhash`.

## `blvm.upstream.v1`

| Method | Returns |
|--------|---------|
| `sources` | One row per configured source: `id`, `kind`, `healthy`, `tip_height`, `tip_hash`, `last_ok_unix`, `capabilities` |
| `tip` | Cached tip for one source |
| `fee_table` | Cached fee table for one source |

## See also

- [blvm-fees](fees.md)
- [Module catalog](overview.md)
