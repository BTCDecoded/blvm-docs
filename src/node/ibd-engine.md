# IBD UTXO engine

Parallel initial block download (IBD) applies blocks through an in-memory UTXO ages pipeline, then a cold **DiskIndex** of spilled segments. Checkpoint exports snapshot that index so a restart does not rebuild from genesis. Serving IBD **to** other peers is [IBD Bandwidth Protection](ibd-protection.md), not this page.

## Scoring clock {#scoring-clock}

Rates on this page are **timestamp BPS**: blocks between two `IBD:` progress prints divided by wall time between those lines (first–last print in the named band). Instant / window p50 is not this clock and is not comparable to a timestamp figure.

## Download {#sync-tuning-guide}

After the bootstrap chunk, the production binary downloads with a moving window. Heights in `[next_needed, next_needed + max_ahead]` are handed out lowest-first. There is no sticky tip owner on this path. The window runs only once bootstrap has finished and `next_needed` is at least `BLVM_IBD_WINDOW_FROM` (default 1). During the bootstrap chunk the legacy assigner still hands out that work.

`BLVM_IBD_ASSIGN=legacy` (also `0` or `off`) keeps the tip-owner assigner for the whole download. Unset, the production binary uses the window.

These switches are on unless turned off:

- **Persist lane.** Body writes run on one thread that batches them. `BLVM_IBD_PERSIST_LANE=0` restores an inline write on the download worker.
- **Deferred drop.** Releasing a connected block’s `Arc` runs off the apply thread. `BLVM_IBD_DEFERRED_DROP=0`, `false`, or `off` restores the inline drop.
- **Prep pool.** `BLVM_IBD_PREP_THREADS` defaults to 2 (clamped to 0–8). Those threads hash transaction ids and fill the output cache ahead of the serial append thread. `0` puts that prep back on the orchestrator.
- **Late body.** A block that arrives after its `GetData` receiver was dropped is still admitted when its hash is in the header index and its height is still inside `[next_needed, next_needed + max_ahead]`. `BLVM_IBD_LATE_BODY_ADMIT=0`, `false`, `off`, or `no` restores discard. Unknown hashes are never admitted.

`BLVM_IBD_TIP_PROBE` and `BLVM_IBD_WIRE_HASH_GATE` stay off unless set. They are not the download path. `BLVM_IBD_HASH_FETCH` has no reader.

## Disk index and checkpoints

Applied blocks spill from the in-memory pipeline into the DiskIndex. A checkpoint export writes a snapshot of that index. A restart loads the snapshot instead of replaying from genesis.

Periodic export waits while the export thread’s 30-second moving average of apply rate stays at or above 200 timestamp BPS. A slower stretch can release the snapshot. While the snapshot is written, the node holds the current download peer: mute and trial stay frozen for that write. The hold is not a long stall by itself.

Once the UTXO set is past about 40 million entries, the interval between exports uses a ceiling of 50,000 blocks. That ceiling is a maximum. If the DiskIndex journal grows past 160 million entries, the interval shrinks, down to a floor of 10,000 blocks, so one compact stays within the cold-write budget.

See also [IBD Bandwidth Protection](ibd-protection.md) (serving) and [Performance — Parallel IBD](performance.md#parallel-initial-block-download-ibd).
