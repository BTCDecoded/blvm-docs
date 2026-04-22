# Testing Infrastructure

## Overview

Bitcoin Commons uses [BLVM Specification Lock](../consensus/formal-verification.md), [property-based testing](property-based-testing.md), [fuzzing](fuzzing.md), integration tests, runtime assertions, and MIRI. Proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Testing Strategy

### Layered Verification

1. **[Formal Verification](../consensus/formal-verification.md)**: Z3 proofs via **BLVM Specification Lock** on spec-locked consensus code
2. **[Property-Based Testing](property-based-testing.md) (Proptest)**: Randomized invariant checks
3. **[Fuzzing](fuzzing.md) (libFuzzer)**: Random input exploration
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

**Code**: [scripts/README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/scripts/README.md) (test data helpers); [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md) (verification workflows)

### Property-Based Tests

Property-based tests verify mathematical invariants:

- **Location**: `tests/consensus_property_tests.rs` and other property test files
- **Coverage**: Mathematical invariants
- **Tool**: Proptest

**Code**: [consensus_property_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/consensus_property_tests.rs)

### Integration Tests

Integration tests verify end-to-end correctness:

- **Location**: `tests/integration/` directory
- **Coverage**: Multi-component scenarios
- **Examples**: BIP compliance, historical replay, mempool mining

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/mod.rs)

### Fuzz tests

Coverage-guided fuzzing (libFuzzer / cargo-fuzz). Inventory: `fuzz/Cargo.toml` in each fuzz crate—see [Fuzzing](fuzzing.md).

### Formal Verification (spec-lock)

[Formal verification](../consensus/formal-verification.md) uses **blvm-spec-lock** / **BLVM Specification Lock** in **blvm-consensus**:

- **Location**: `src/`, `tests/`
- **Command**: `cargo spec-lock verify` (tiered: strong / medium / slow)
- **Inventory**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)
- **Tool**: [blvm-spec-lock](https://github.com/BTCDecoded/blvm-spec-lock)

**See also**: [UTXO Commitments](../consensus/utxo-commitments.md#utxo-proof-verification)

**Code**: [formal-verification.md](../consensus/formal-verification.md)

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

**Code**: [formal-verification.md](../consensus/formal-verification.md)

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

**Code**: [tests/](https://github.com/BTCDecoded/blvm-consensus/tree/main/tests)

## Edge Case Coverage

### Beyond Proof Bounds

Edge cases beyond blvm-spec-lock proof bounds are covered by:

1. **Property-Based Testing**: Random inputs of various sizes
2. **Mainnet Block Tests**: Real Bitcoin mainnet blocks
3. **Integration Tests**: Realistic scenarios
4. **Fuzz Testing**: Random generation

**Code**: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)

## Differential Testing

### Cross-implementation checks

Differential tests compare **blvm-consensus** with an independent full node over RPC (see [Differential testing](differential-testing.md)).

- **Location**: `tests/integration/differential_tests.rs` (skeleton); full harnesses in **blvm-bench**
- **Purpose**: Catch consensus divergences empirically

**Code**: [differential_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs)

## CI Integration

### Automated Testing

All tests run in CI:

- **Unit Tests**: Required for merge
- **Property Tests**: Required for merge
- **Integration Tests**: Required for merge
- **Fuzz Tests**: Run on schedule
- **blvm-spec-lock Proofs**: Run separately, not blocking
- **MIRI**: Run on property tests and critical unit tests

**Code**: [formal-verification.md](../consensus/formal-verification.md)

## Test Metrics

- **Property Test Functions**: Multiple functions across all files
- **Runtime Assertions**: Multiple assertions (`assert!` and `debug_assert!`)
- **Fuzz Targets**: Multiple fuzz targets

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Location**: `blvm-consensus/tests/`, `blvm-consensus/fuzz/`, `blvm-consensus/src/`

## See Also

- [Property-Based Testing](property-based-testing.md) - Verify mathematical invariants
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Differential Testing](differential-testing.md) - Cross-check vs reference RPC
- [Benchmarking](benchmarking.md) - Performance measurement
- [Snapshot Testing](snapshot-testing.md) - Output consistency verification
- [Formal Verification](../consensus/formal-verification.md) - blvm-spec-lock model checking
- [UTXO Commitments](../consensus/utxo-commitments.md#utxo-proof-verification) - Spec-lock verification for UTXO operations
- [Contributing](contributing.md) - Testing requirements for contributions
