# Differential Testing

## Overview

Differential testing compares **blvm-consensus** validation results against an **independent full node** over JSON-RPC, so disagreements surface as empirical failures. Primary tooling lives in **`blvm-bench`** (parallel runs, harnesses, optional reference-binary integration).

## Purpose

- **Cross-check** local validation vs an external node’s `testmempoolaccept`, `submitblock`, etc.
- **Catch divergences** before mainnet exposure
- **Exercise** real blocks and scripted scenarios, not only unit tests

## Implementation

**Primary:** [`blvm-bench`](https://github.com/BTCDecoded/blvm-bench) — differential harnesses, regtest helpers, RPC client, historical/BIP-focused tests.

**Skeleton in consensus:** [`differential_tests.rs`](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs) — placeholder; use **`blvm-bench`** for real runs.

## Comparison flow

1. Validate in **blvm-consensus**.
2. Submit the same payload to a **reference RPC** (configure URL/credentials for your environment).
3. Compare accept/reject and errors; treat any mismatch as a bug or intentional policy difference to document.

Rust-shaped APIs in docs may use names like `CoreRpcConfig` in code—**configure whatever full node you use for cross-validation**; this documentation does not require a specific vendor.

## Differential fuzzing (internal)

The `differential_fuzzing` **cargo-fuzz** target checks **internal** consistency (round-trips, idempotence). It does **not** call an external node. See [Fuzzing](fuzzing.md) and [`differential_fuzzing.rs`](https://github.com/BTCDecoded/blvm-consensus/blob/main/fuzz/fuzz_targets/differential_fuzzing.rs).

## Public JSON test vectors

Consensus tests reuse **widely circulated** transaction/script JSON vectors (same families many implementations use). Paths and provenance: [`TEST_DATA_SOURCES.md`](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/TEST_DATA_SOURCES.md) in **blvm-consensus**.

## Mainnet and historical tests

Real mainnet blocks and era-specific scenarios are exercised in integration and bench tooling; see **blvm-consensus** `tests/` and **blvm-bench** for entry points.

## Running (bench)

```bash
cd blvm-bench
cargo test --features differential
# or targeted suites as provided by blvm-bench
```

**Prerequisites:** a **reference full node** binary and RPC reachable from the harness when RPC comparison is enabled; see **blvm-bench** README for env vars (e.g. path to the binary, RPC URL).

## Results

Treat **divergence** as: investigate, fix consensus if BLVM is wrong, or document **policy** differences (mempool policy is not identical across implementations).

## See also

- [Testing](testing.md)
- [Fuzzing](fuzzing.md)
- [Formal verification](../consensus/formal-verification.md)
