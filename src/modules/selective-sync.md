# Selective Synchronization Module

The **blvm-selective-sync** module provides a configurable **sync policy**: operators can avoid serving or persisting certain flagged transaction content during IBD while keeping full cryptographic validation of the chain.

## Requirements

- Node with modules enabled; **blvm-selective-sync** built and installed (see [Module catalog](overview.md#installing-modules)).
- Typical workspace: **blvm-node**, **blvm-sdk**, **blvm-protocol** (path dependencies via `[patch.crates-io]` in the module crate for local builds).

## Loading

Pin and optional spawn overrides use manifest name **`blvm-selective-sync`**:

```toml
transport_preference = "tcponly"

[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-selective-sync = "0.1.*"
```

After load, the module registers **`blvm sync-policy …`** CLI with the node (`getmoduleclispecs`).

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

**Auth:** Module CLI calls admin RPC (`runmodulecli`). Pass the **same `--config`** as the running node; the CLI uses `[rpc_auth].admin_tokens` (Bearer), `tokens`, or `username`/`password` from that file — see [Quick Start](../getting-started/quick-start.md).

## Local development (workspace builds)

Release **governance** builds verify native module binaries against the GitHub registry checksums when `[modules].registry_url` is set (the default). A locally built copy under `modules_dir` **without** a `[binary].hash` in `module.toml` will fail **auto-load** with a registry lookup error even though the files are on disk.

For workspace testing:

- Install the built binary under `modules/blvm-selective-sync/` with matching `module.toml`, **and** either:
  - add a `[binary].hash` for the built artifact, **or**
  - clear the default registry: `registry_url = ""` in `[modules]`, **or**
  - bootstrap from the published registry (pin + default `registry_url`).
- Confirm load with `listmodules` (non-empty) before `blvm sync-policy …`; `runmodulecli` blocks while the module subprocess is down.
- **`loadmodule`** uses the same **`ModuleLoader`** discovery and checksum path as auto-load (registry governance when `registry_url` is set). The module must stay running; a crash removes it from `listmodules` immediately.

## Configuration

Module `config.toml` (under `<modules.data_dir>/blvm-selective-sync/`; overridable via `[modules.blvm-selective-sync]`):

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
