# Testing Infrastructure

## Overview

Bitcoin Commons uses [BLVM Specification Lock](../consensus/formal-verification.md), [property-based testing](property-based-testing.md), [fuzzing](#fuzzing), integration tests, runtime assertions, and MIRI. Proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Testing Strategy

### Layered Verification

1. **[Formal Verification](../consensus/formal-verification.md)**: Z3 proofs via **BLVM Specification Lock** on spec-locked consensus code
2. **[Property-Based Testing](property-based-testing.md) (Proptest)**: Randomized invariant checks
3. **[Fuzzing](#fuzzing) (libFuzzer)**: Random input exploration
4. **Integration Tests**: End-to-end scenarios
5. **Unit Tests**: Per-function tests
6. **Runtime Assertions**: Optional invariant checks (feature-gated)
7. **MIRI**: Undefined-behavior detection on selected tests

## Test Types

### Unit Tests

Unit tests verify individual functions in isolation:

- **Location**: `tests/` directory, `#[test]` functions
- **Coverage**: Public functions
- **Examples**: Transaction validation, block validation, script execution


### Property-Based Tests

Property-based tests verify mathematical invariants:

- **Location**: `tests/consensus_property_tests.rs` and other property test files
- **Coverage**: Mathematical invariants
- **Tool**: Proptest


### Integration Tests

Integration tests verify end-to-end correctness:

- **Location**: `tests/integration/` directory
- **Coverage**: Multi-component scenarios
- **Examples**: BIP compliance, historical replay, mempool mining


### Fuzzing {#fuzzing}

Coverage-guided fuzzing uses **libFuzzer** via **cargo-fuzz** on unstructured byte inputs. It complements spec-lock, unit tests, and property tests; it does not replace them.

#### Source of truth

Harness names and crate wiring live in each repo’s **`fuzz/Cargo.toml`** (`[[bin]]` entries). Implementation sources are under **`fuzz/fuzz_targets/`**. Do not treat prose (here or in READMEs) as an inventory—it goes stale.

| Crate | Location |
|-------|----------|
| blvm-consensus | [`blvm-consensus/fuzz`](https://github.com/BTCDecoded/blvm-consensus/tree/main/fuzz) |
| blvm-protocol | [`blvm-protocol/fuzz`](https://github.com/BTCDecoded/blvm-protocol/tree/main/fuzz) |
| blvm-node | [`blvm-node/fuzz`](https://github.com/BTCDecoded/blvm-node/tree/main/fuzz) |
| blvm-sdk | [`blvm-sdk/fuzz`](https://github.com/BTCDecoded/blvm-sdk/tree/main/fuzz) |

Local monorepo checkouts often use **`[patch.crates-io]`** in **`fuzz/Cargo.toml`** so fuzz crates resolve **path** dependencies; **continuous integration** may build fuzz targets against **crates.io** instead (see comments in each repo’s **`fuzz/Cargo.toml`**—for example **`blvm-consensus/fuzz`** and **`blvm-protocol/fuzz`**).

#### Quick start (consensus)

```bash
cd blvm-consensus/fuzz
./init_corpus.sh    # optional: seed corpora
cargo +nightly fuzz run <target_name>
```

Pick `<target_name>` from `fuzz/Cargo.toml`. The `fuzz/` directory also contains scripts (e.g. campaign runners, corpus helpers, sanitizer build helpers)—use what matches your workflow.

#### CI

Fuzz jobs are defined in the relevant repository’s GitHub Actions. Matrix steps and timeouts may not exercise every harness on every run; read the workflow for actual behavior.

### Formal Verification (spec-lock)

[Formal verification](../consensus/formal-verification.md) uses **blvm-spec-lock** / **BLVM Specification Lock** in **blvm-consensus**:

- **Location**: `src/`, `tests/`
- **Command**: `cargo spec-lock verify` (tiered: strong / medium / slow)
- **Inventory**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)
- **Tool**: [blvm-spec-lock](https://github.com/BTCDecoded/blvm-spec-lock)

**See also**: [UTXO Commitments](../node/utxo-commitments.md#formal-verification)


### Runtime Assertions

Runtime assertions catch violations during execution:

- **Coverage**: Critical paths with runtime assertions
- **Production**: Available via feature flag

### MIRI Integration

MIRI detects undefined behavior:

- **CI Integration**: Automated undefined behavior detection
- **Coverage**: Property tests and critical unit tests
- **Tool**: MIRI interpreter

## Coverage Statistics

### Overall Coverage

| Verification Technique | Status |
|----------------------|--------|
| **Formal Proofs (spec-lock)** | ✅ Tiered Z3 proofs on spec-locked code |
| **Property Tests** | ✅ Broad invariant coverage |
| **Runtime Assertions** | ✅ Feature-gated on selected paths |
| **Fuzz Targets** | ✅ Critical validation surfaces |
| **MIRI Integration** | ✅ UB checks on selected tests |
| **Mathematical Specs** | ✅ Orange Paper + docs |

### Coverage by Consensus Area

Economic rules, PoW, transactions, blocks, scripts, reorg, crypto, mempool, SegWit, and serialization are covered by unit, property, integration, and fuzz tests, with **BLVM Specification Lock** on critical spec-locked paths. Details: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md).

## Running Tests

### Run All Tests

```bash
cd blvm-consensus
cargo test
```

### Run Specific Test Type

```bash
# Unit tests
cargo test --lib

# Property tests
cargo test --test consensus_property_tests

# Integration tests
cargo test --test integration

# Fuzz (example; target name from fuzz/Cargo.toml)
cd fuzz && cargo +nightly fuzz run <target_name>
```

### Run with MIRI

```bash
cargo +nightly miri test
```

### Run blvm-spec-lock Proofs

```bash
cargo spec-lock verify
```


### Run Spec-Lock Verification

```bash
# Run spec-lock verification (requires cargo-spec-lock)
cargo spec-lock verify --crate-path .
```

## Coverage Goals

### Target Coverage

Ongoing expansion of spec-lock coverage, property tests, fuzz corpora, runtime assertions, and integration scenarios. Status: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md), [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Test Organization

### Directory Structure

```
blvm-consensus/
├── src/                    # Source; spec-lock on marked functions
├── tests/
│   ├── consensus_property_tests.rs  # Main property tests
│   ├── integration/         # Integration tests
│   ├── unit/               # Unit tests
│   ├── fuzzing/            # Fuzzing helpers
│   └── verification/       # Verification tests
└── fuzz/
    └── fuzz_targets/        # Fuzz targets
```


## Edge Case Coverage

### Beyond Proof Bounds

Edge cases beyond blvm-spec-lock proof bounds are covered by:

1. **Property-Based Testing**: Random inputs of various sizes
2. **Mainnet Block Tests**: Real Bitcoin mainnet blocks
3. **Integration Tests**: Realistic scenarios
4. **Fuzz Testing**: Random generation


## Differential Testing

Cross-implementation checks compare BLVM validation with Bitcoin Core (RPC, historical replay, and a two-phase full-chain program). Primary harness: [**blvm-bench**](https://github.com/BTCDecoded/blvm-bench) `tests/integration.rs`; consensus stub: [`differential_tests.rs`](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs).

```bash
cd blvm-bench
cargo test --test integration --features differential
```

See [Differential Testing](differential-testing.md) for layers (BIP/regtest, historical, full-chain Phase 1/2), env vars, and operator docs.


## CI Integration

### Automated Testing

All tests run in CI:

- **Unit Tests**: Required for merge
- **Property Tests**: Required for merge
- **Integration Tests**: Required for merge
- **Fuzz Tests**: Run on schedule
- **Differential Tests**: **blvm-bench** integration suite (self-hosted workflow currently paused; see [differential-testing.md](differential-testing.md))
- **blvm-spec-lock Proofs**: Run separately, not blocking
- **MIRI**: Run on property tests and critical unit tests


## Test Metrics

- **Property Test Functions**: Multiple functions across all files
- **Runtime Assertions**: Multiple assertions (`assert!` and `debug_assert!`)
- **Fuzz Targets**: Multiple fuzz targets


## Components

The testing infrastructure includes:
- Unit tests for all public functions
- Property-based tests for mathematical invariants
- Integration tests for end-to-end scenarios
- Fuzz tests for edge case discovery
- blvm-spec-lock proofs for formal verification
- Runtime assertions for execution-time checks
- MIRI integration for undefined behavior detection
- Differential tests (see [differential-testing.md](differential-testing.md))


## Source

- [scripts/README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/scripts/README.md) (test data helpers); [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md) (verification workflows)
- [consensus_property_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/consensus_property_tests.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/mod.rs)
- [formal-verification.md](../consensus/formal-verification.md)
- [tests/](https://github.com/BTCDecoded/blvm-consensus/tree/main/tests)
- [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)
- [differential_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs) (consensus stub)
- [blvm-bench integration tests](https://github.com/BTCDecoded/blvm-bench/blob/main/tests/integration.rs), [FULL_CHAIN_DIFFERENTIAL.md](https://github.com/BTCDecoded/blvm-bench/blob/main/docs/FULL_CHAIN_DIFFERENTIAL.md)
- [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)
- [blvm-consensus/tests/](https://github.com/BTCDecoded/blvm-consensus/tree/main/tests/), [blvm-consensus/fuzz/](https://github.com/BTCDecoded/blvm-consensus/tree/main/fuzz/), [blvm-consensus/src/](https://github.com/BTCDecoded/blvm-consensus/tree/main/src/) (blvm-consensus/fuzz/blvm-consensus/src/`)
## See Also

- [Property-Based Testing](property-based-testing.md) - Verify mathematical invariants
- [Differential Testing](differential-testing.md) - Cross-check vs Core (RPC, historical, full-chain)
- [Benchmarking](benchmarking.md) - Performance measurement
- [Snapshot Testing](snapshot-testing.md) - Output consistency verification
- [Formal Verification](../consensus/formal-verification.md) - blvm-spec-lock model checking
- [UTXO Commitments](../node/utxo-commitments.md#formal-verification) - Spec-lock verification for UTXO operations
- [Contributing](contributing.md) - Testing requirements for contributions
