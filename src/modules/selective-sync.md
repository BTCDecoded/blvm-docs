# Selective Synchronization Module

The **blvm-selective-sync** module provides a configurable **IBD sync policy**: operators can avoid downloading certain flagged transaction content during initial block download while keeping full cryptographic validation of the chain. It integrates with the [spam filter](../consensus/spam-filtering.md) and registry concepts in blvm-protocol.

## Requirements

- Node with modules enabled; **blvm-selective-sync** built and installed (see [Modules Overview](overview.md#installing-modules)).
- Typical workspace: **blvm-node**, **blvm-sdk**, **blvm-protocol** (path dependencies).

## Loading

Enable the module in node configuration (same patterns as other modules). After load, the module registers CLI with the node.

## User-facing CLI (`blvm sync-policy …`)

With the module running, the **blvm** binary exposes subcommands (forwarded to the module over IPC). Examples:

| Command | Purpose |
|---------|---------|
| `blvm sync-policy list` | List subscribed registries and last refresh |
| `blvm sync-policy subscribe <url>` | Subscribe to a registry URL |
| `blvm sync-policy unsubscribe <url>` | Remove a registry |
| `blvm sync-policy refresh` | Refresh subscribed registries |
| `blvm sync-policy status` | Policy / sync status |
| `blvm sync-policy config-path` | Print path to policy config (e.g. for editing `sync-policy.json`) |
| `blvm sync-policy build-entry …` | Build a registry entry from transaction data (testing / tooling) |
| `blvm sync-policy build-registry …` | Build registry from block data with a spam-filter preset |

Exact flags vary by build; use `blvm sync-policy --help` when the module is loaded.

## Configuration

- Policy and registry URLs are managed via the commands above; config lives under the module data directory (see `config-path`).
- Node may override module storage via `[modules.selective-sync]` (e.g. `database_backend`); see [Node configuration](../node/configuration.md).

## Implementation notes

- Built with the [SDK declarative style](../sdk/module-development.md#sdk-declarative-style-recommended): `#[module]`, `#[command]`, `run_module!`.
- **Withholding and P2P serve policy:** policy logic can merge **block hashes** (and related sets) into the node’s **`merge_block_serve_denylist`** path via `NodeAPI` so that, after IBD gates, `getdata` for those hashes does not serve full `block` messages to peers (`notfound`), while consensus validation behavior remains unchanged. Transaction-level withholding uses the parallel **`merge_tx_serve_denylist`** surface when enabled for the build. See [Module development](../sdk/module-development.md#querying-node-data) (P2P serve policy & sync) and [Module IPC Protocol](../architecture/module-ipc-protocol.md).
- Repository: [blvm-selective-sync](https://github.com/BTCDecoded/blvm-selective-sync).

## See also

- [Modules overview](overview.md)
- [Module development](../sdk/module-development.md)
- [Parallel IBD / performance](../node/performance.md)
