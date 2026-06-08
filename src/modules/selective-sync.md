# Selective Synchronization Module

The **blvm-selective-sync** module provides a configurable **sync policy**: operators can avoid serving or persisting certain flagged transaction content during IBD while keeping full cryptographic validation of the chain.

## Requirements

- Node with modules enabled; **blvm-selective-sync** built and installed (see [Modules Overview](overview.md#installing-modules)).
- Typical workspace: **blvm-node**, **blvm-sdk**, **blvm-protocol** (path dependencies via `[patch.crates-io]` in the module crate for local builds).

## Loading

Enable the module in node configuration (same patterns as other modules). After load, the module registers CLI with the node.

## User-facing CLI (`blvm sync-policy …`)

| Command | Purpose |
|---------|---------|
| `blvm sync-policy list` | List subscribed registries |
| `blvm sync-policy subscribe <url>` | Subscribe to a registry URL |
| `blvm sync-policy unsubscribe <url>` | Remove a registry |
| `blvm sync-policy refresh` | Fetch registries, quorum-merge, auto-apply denylists |
| `blvm sync-policy apply` | Re-apply serve denylists from stored policy |
| `blvm sync-policy status` | Policy counts, denylist snapshots, IBD filter state |
| `blvm sync-policy export-registry` | Export merged policy JSON |
| `blvm sync-policy config-path` | Path to module `config.toml` |
| `blvm sync-policy build-entry …` | Build registry entry from transaction hex |
| `blvm sync-policy build-registry …` | Build registry from block with spam-filter preset |

Use `blvm sync-policy --help` when the module is loaded for current flags.

## Configuration

Module `config.toml` (under module data dir; overridable via `[modules.selective-sync]`):

| Key | Purpose |
|-----|---------|
| `registries` | Registry URLs |
| `min_registry_agreement` | Quorum threshold (0.0–1.0) |
| `registry_refresh_interval` | Periodic refresh interval (seconds) |
| `witness_mode` | `strict` (default) or `relaxed` |
| `ibd_filter_enabled` | Strip flagged witnesses during IBD persistence |
| `on_chain_registry_builder` | Index flagged txs from each `NewBlock` |
| `audit_log` / `audit_log_path` | Optional audit trail |

Example — enable IBD witness filtering:

```toml
ibd_filter_enabled = true
witness_mode = "strict"
registries = ["https://example.com/registry.json"]
```

Workflow:

```bash
blvm sync-policy subscribe https://example.com/registry.json
blvm sync-policy refresh
blvm sync-policy status
```

## Serve policy (P2P)

After `refresh` or `apply`, merged tx/block hashes are pushed to the node via `merge_tx_serve_denylist` and `merge_block_serve_denylist`. Peers requesting denied hashes receive `notfound` for full block/tx relay. Requires `network_access` / `read_network` capabilities.

## IBD witness filter

When `ibd_filter_enabled = true`, the module exposes **`filter_block_before_store`** via `ModuleAPI`. During parallel IBD, the node calls this hook before writing witness blobs to the blockstore. Flagged witness stacks are emptied; the module publishes `IBDBlockFiltered` events.

The node integration is generic (`blvm-node` `module/pipeline.rs`) — not selective-sync-specific code in `parallel_ibd/`. On IPC failure the node **fail-opens** (stores unfiltered data).

## Implementation notes

- Binary uses `run_module_with_setup_and_api` (mesh pattern) for CLI + ModuleAPI IPC.
- Periodic refresh uses module-local `tokio::interval` in `setup` — not `register_timer`.
- Repository: [blvm-selective-sync](https://github.com/BTCDecoded/blvm-selective-sync).

## See also

- [Modules overview](overview.md)
- [Module development](../sdk/module-development.md)
- [Parallel IBD / performance](../node/performance.md)
