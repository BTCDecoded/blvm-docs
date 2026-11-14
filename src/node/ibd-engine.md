# IBD UTXO engine

## Sync tuning guide

First mainnet sync always starts from [First Node Setup: Mainnet IBD](../getting-started/first-node.md#mainnet-initial-sync) (release IBD example config). For other IBD topics, use the [operator IBD hub](../getting-started/operator-guide.md#initial-block-download-ibd) or:

| Topic | Page |
|-------|------|
| Parallel download, pipelining, assume-valid | [Performance optimizations](performance.md) |
| `[ibd]` keys and `BLVM_IBD_*` | [Configuration reference: IBD](../reference/configuration-reference.md#ibd-configuration) |
| Serving-side bandwidth limits | [IBD bandwidth protection](ibd-protection.md) |
| LAN Core / same-subnet peers | [LAN peering](lan-peering.md) |
| Chainstate backend and `data_dir` | [Storage backends](storage-backends.md) |

## Overview

During parallel initial block download (IBD), the node validates blocks in height order while downloading from one or more peers. By default, the **age-tiered UTXO engine** holds live UTXOs in memory and on disk under `<data_dir>/ibd_engine/`, with mid-sync checkpoints for crash-safe resume. The legacy in-process store remains available as an opt-out.

## Enable (default)

The engine is **on by default**. Stable table path: `<data_dir>/ibd_engine/utxo_table.bin` (override with `BLVM_IBD_ENGINE_PATH`).

**Opt-out:**

```bash
export BLVM_IBD_ENGINE=0
```

`[ibd] utxo_engine = false` does the same. `BLVM_IBD_ENGINE` wins over the file.

Optional environment variables:

| Variable | Purpose |
|----------|---------|
| `BLVM_IBD_ENGINE_PATH` | Path to the engine flat table (default: `<data_dir>/ibd_engine/utxo_table.bin`) |
| `BLVM_IBD_CHECKPOINT_INTERVAL` | Fixed block interval for mid-IBD checkpoint export (engine mode) |
| `BLVM_IBD_DEFER_CHECKPOINT_INTERVAL` | RAM-tier default override for deferred checkpoint spacing |
| `BLVM_IBD_EXPORT_HEIGHT_OVERRIDE` | Force resume/export height only when it is at least the stored export height. An override below that height is ignored. `start-ibd-mainnet.sh` strips an inherited override unless `BLVM_ALLOW_EXPORT_HEIGHT_OVERRIDE=1`. |

Download scheduling still uses **[parallel IBD](performance.md#parallel-initial-block-download-ibd)** (`[ibd].mode = "parallel"`). The engine replaces how validated blocks apply UTXO changes during that pipeline.

## Architecture

1. **Index and table**: Age-tiered structures track live UTXOs and support fast spend lookups during validation.
2. **Spend session**: Batches spend/create operations per block and feeds the engine from the validation loop.
3. **Checkpoint export**: Periodic snapshots of engine state allow resume after interruption without re-downloading from genesis.
4. **Import / seed**: On restart, the node seeds validation from the last exported checkpoint height when present.


## Operator notes

- Use the **same** `storage.data_dir` on every run; do not delete the active database backend directory (`heed3/`, `rocksdb/`, …) mid-sync.
- On **SIGTERM** / **SIGINT** during parallel IBD, the node drains in-flight validation and flushes the UTXO watermark before exit when possible.
- **`io_uring`** accelerates engine table I/O on **Linux**; other platforms use a `pread` fallback (engine still runs on Windows).
- **[Assume-valid](../reference/configuration-reference.md#block_validationassume_valid_height)** skips signature verification below the configured height when the hash is set and chainwork meets the minimum. The mainnet seed sets that hash at height **912683**. Block structure, Merkle roots, and proof-of-work are still checked.
- Tune `[ibd]` or `BLVM_IBD_*` only when you need explicit peer or mode control. The map is the [sync tuning guide](#sync-tuning-guide).

## Source

- [ibd_engine/](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/ibd_engine/), [parallel_ibd/validation_loop.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/validation_loop.rs)
- [ibd_engine/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/ibd_engine/mod.rs), [spend_session.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/ibd_engine/spend_session.rs), [export.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/ibd_engine/export.rs)
