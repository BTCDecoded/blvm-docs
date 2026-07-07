# Differential Testing

## Overview

Differential testing compares BLVM validation against an independent reference—primarily Bitcoin Core—so consensus disagreements show up as test failures. Tooling lives in [**blvm-bench**](https://github.com/BTCDecoded/blvm-bench). A local stub in [`blvm-consensus/tests/integration/differential_tests.rs`](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs) defers to bench for RPC and full-chain work.

This complements [formal verification](../consensus/formal-verification.md), [property-based testing](property-based-testing.md), and [fuzzing](testing.md#fuzzing).

## Consensus vs policy

| In scope | Out of scope |
|----------|--------------|
| Block accept/reject, script execution on canonical blocks, UTXO updates in `connect_block` | Mempool policy, P2P, wallet |

Consensus mismatches are bugs. Mempool-policy mismatches may be intentional—document them.

## Layers

| Layer | Entry point | Compares |
|-------|-------------|----------|
| **Integration / BIP** | `tests/integration.rs` | BLVM vs Core RPC on regtest blocks (BIP30, BIP34, BIP90, valid block) |
| **Historical replay** | `test_historical_blocks_differential` | Real mainnet blocks over a height range vs Core RPC or chunk cache |
| **Per-input script** | `script_validation.rs` | BLVM vs `libbitcoinconsensus` when prevouts are known |
| **Full-chain Phase 1** | `sort_merge_test` step 6 | Every non-coinbase script on canonical mainnet |
| **Full-chain Phase 2** | `block_kernel_diff` | BLVM `connect_block` vs `libbitcoinkernel` `process_block` |
| **Internal fuzz** | `differential_fuzzing` | Round-trips inside blvm-consensus (no external node) |

The **full-chain program** (Phase 1 + Phase 2) is the mainnet consensus differential. Integration and historical tests are faster dev/CI loops.

**Full-chain status:** Phase 1 and Phase 2 are **operator-driven** (resource-intensive; default target height ~900,000 blocks in `blvm-bench` tooling). They are complementary to spec-lock: local Z3 obligations on annotated functions vs global empirical agreement with Core across history. The self-hosted differential CI workflow may be paused—do not assume full-chain zero-divergence claims are CI-gated to chain tip without checking current operator logs. Clean runs: Phase 1 step 6 `Failed: 0`; Phase 2 per-height `"match": true`.

Operator detail: [`docs/FULL_CHAIN_DIFFERENTIAL.md`](https://github.com/BTCDecoded/blvm-bench/blob/main/docs/FULL_CHAIN_DIFFERENTIAL.md), [`README_DIFFERENTIAL_TESTING.md`](https://github.com/BTCDecoded/blvm-bench/blob/main/README_DIFFERENTIAL_TESTING.md).

## Integration tests

Regtest tests start a Core node, validate with BLVM, and compare via RPC (`testmempoolaccept`, `submitblock` in `differential.rs`).

```bash
cd blvm-bench
cargo test --test integration --features differential
```

Remote RPC (auto-discovery off):

```bash
export BITCOIN_RPC_HOST=node.example.com BITCOIN_RPC_PORT=8332
export BITCOIN_RPC_USER=rpcuser BITCOIN_RPC_PASSWORD=rpcpassword
export BITCOIN_NETWORK=mainnet BITCOIN_AUTO_DISCOVER=false
cargo test --test integration --features differential
```

Filter BIP tests: `cargo test --test integration test_bip --features differential`.

Tests **skip** Core comparison when no Core binary or RPC is found (`CORE_PATH`, standard install paths, or auto-discovery via `NodeDiscovery`).

## Historical replay

```bash
HISTORICAL_BLOCK_START=0 HISTORICAL_BLOCK_END=1000 \
  cargo test --test integration test_historical_blocks_differential --features differential
```

Optional: `PARALLEL_WORKERS`, `CHUNK_SIZE`, `BLOCK_CACHE_DIR`. With `BLOCK_CACHE_DIR` set (or large ranges without RPC), the harness uses parallel chunk replay. Pruned nodes are detected via `getpruninginfo`; start height is adjusted to available blocks.

## Full-chain program (two phases)

Mainnet validation is split because running every script inside every `connect_block` is impractical at scale.

```text
connect_block  ≈  script_checks (Phase 1)  +  block rules (Phase 2)
```

| Phase | Tool | Checks |
|-------|------|--------|
| **1** | `sort_merge_test` step 6 | BLVM `verify_script_with_context_full` on every non-coinbase input |
| **2** | `block_kernel_diff` | Per-block accept/reject vs `libbitcoinkernel` |

Phase 1 reference is the **canonical chain** (Core already accepted these blocks)—not per-input `bitcoinconsensus`. Phase 2 can skip scripts on **both** sides via `--blvm-assume-valid-height` and `--kernel-skip-scripts` so block rules are not re-checked after Phase 1; CLI defaults for assume-valid are **off** (`0`).

**Phase 1** — build and run step 6 after steps 1–5 produce `joined_sorted.bin`:

```bash
cargo build --release --features differential --bin sort_merge_test
export BLOCK_CACHE_DIR=/path/to/chunk-cache START_HEIGHT=0 END_HEIGHT=<tip>
./target/release/sort_merge_test step6
```

Clean run: step 4 `Unmatched inputs: 0`; step 6 `Failed: 0`, progress `M:0 F:0 E:0`.

**Phase 2** — requires `libbitcoinkernel` (`BITCOIN_CORE_LIB_DIR`):

```bash
cargo build --release --features bitcoinkernel --bin block_kernel_diff
```

Clean run: per-height JSONL with `"match": true`; empty `*.divergences.jsonl`. Bootstrap, checkpoints, and parallel lanes: [`block_kernel_diff.rs`](https://github.com/BTCDecoded/blvm-bench/blob/main/src/bin/block_kernel_diff.rs) module docs and `scripts/restart-kernel-diff-500k.sh`.

## Other checks

- **`script_validation.rs`** — targeted BLVM vs `bitcoinconsensus` (`differential` feature); not the Phase 1 engine.
- **JSON vectors** — blvm-consensus unit tests; provenance in [`TEST_DATA_SOURCES.md`](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/TEST_DATA_SOURCES.md).
- **Internal fuzz** — `cd blvm-consensus/fuzz && cargo +nightly fuzz run differential_fuzzing` ([Fuzzing](testing.md#fuzzing)).

## CI

[`.github/workflows/differential-tests.yml`](https://github.com/BTCDecoded/blvm-bench/blob/main/.github/workflows/differential-tests.yml) on a self-hosted runner is **paused** (`workflow_dispatch` only; job `if: false`). When enabled, it runs `cargo test --test integration --features differential`. Full-chain phases are operator-driven.

## Limitations

- Some integration paths note imperfect block wire serialization for Core submission; violation detection still applies ([README_DIFFERENTIAL_TESTING.md](https://github.com/BTCDecoded/blvm-bench/blob/main/README_DIFFERENTIAL_TESTING.md)).
- Phase 2 needs a block index covering the compared height range.

## See also

- [Testing](testing.md)
- [Fuzzing](testing.md#fuzzing)
- [Formal Verification](../consensus/formal-verification.md)
