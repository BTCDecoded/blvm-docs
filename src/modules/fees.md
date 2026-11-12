# Fee estimators (`blvm-fees`)

`blvm-fees` publishes two named fee estimators to the node: `blend` and `blend-min`. `blend` follows LN-Zap `mergeFeeEstimates`. `blend-min` takes the per-target minimum, then a prefix minimum, so a longer target never quotes more than a shorter one. Every rate is an integer in sat/kvB.

It is **not** a default module pin, and it is not in `registry/modules.json`. External fee data stays off until the operator selects an estimator. Source: [BTCDecoded/blvm-fees](https://github.com/BTCDecoded/blvm-fees). Crate: `blvm-fees` on crates.io.

## Inputs

- The node's native fee table (always).
- `blvm.upstream.v1` from [blvm-upstream](upstream.md), when that module is loaded. If upstream data is missing, the module still submits a table built from the native quotes. `blvm-fees` makes no HTTP requests itself; upstream fetches need a `blvm` built with `--features blvm-node/module-http` (see [blvm-upstream](upstream.md)).

An upstream source whose height is more than `max_height_delta` blocks behind the best source is dropped before merging. The remaining sources are ordered by `priority`.

## Manifest

`module.toml` declares the capabilities `subscribe_events`, `discover_modules`, `call_module`, `read_mempool`, and `write_fee_estimates`, `requires_apis = ["blvm.upstream.v1"]`, and two `[[fee_estimators]]` entries (`blend`, `blend-min`) with modes `conservative` and `economical` and `default_merge = "replace"`.

## Configuration

The module reads `<module data dir>/config.toml`. The scalar keys can also come from `[modules.blvm-fees]` in the node config. The `priority` array stays in the module file.

```toml
priority = ["mempool-space", "native", "blockstream"]  # default
max_height_delta = 3
request_timeout_ms = 5000
submit_interval_secs = 10
```

## Selecting it on the node

The node only uses a module estimator when `[fees]` selects it. See [Fee estimator](../reference/configuration-reference.md#fee-estimator-fees).

```toml
[fees]
estimator = "blend"
fallback = "native"      # serve native quotes when the blend table is missing or stale

[fees.external]
ttl_secs = 120           # a stored table older than this is stale
max_lag_blocks = 1

# [fees.external.blend]
# mode = "lower_only"    # or "replace"; absent keeps the module's default_merge
```

`listfeeestimators` shows whether `blend` is registered and fresh. `estimatesmartfee` with verbosity 1 reports `source` (`external`, `external_min`, …), `requested_estimator`, `active_estimator`, and `degraded`. See [RPC API: Fee estimation](../node/rpc-api.md#fee-estimation).

## See also

- [blvm-upstream](upstream.md)
- [Module catalog](overview.md)
