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
- Repository: [blvm-selective-sync](https://github.com/BTCDecoded/blvm-selective-sync).

## See also

- [Modules overview](overview.md)
- [Module development](../sdk/module-development.md)
- [Parallel IBD / performance](../node/performance.md)
