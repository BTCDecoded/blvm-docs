# Testing Infrastructure

## Overview

Bitcoin Commons uses a multi-layered testing strategy combining [formal verification](../consensus/formal-verification.md), [property-based testing](property-based-testing.md), [fuzzing](fuzzing.md), integration tests, and runtime assertions. This approach ensures correctness across consensus-critical code.

## Testing Strategy

### Layered Verification

The testing strategy uses multiple complementary techniques:

1. **[Formal Verification](../consensus/formal-verification.md)**: Proves correctness for all inputs (bounded)
2. **[Property-Based Testing](property-based-testing.md) (Proptest)**: Verifies invariants with random inputs (unbounded)
3. **[Fuzzing](fuzzing.md) (libFuzzer)**: Discovers edge cases through random generation
4. **Integration Tests**: Verifies end-to-end correctness
5. **Unit Tests**: Tests individual functions
6. **Runtime Assertions**: Catches violations during execution
7. **MIRI Integration**: Detects undefined behavior

**Code**: [CONSENSUS_COVERAGE_ASSESSMENT.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/CONSENSUS_COVERAGE_ASSESSMENT.md#L1-L196)

## Test Types

### Unit Tests

Unit tests verify individual functions in isolation:

- **Location**: `tests/` directory, `#[test]` functions
- **Coverage**: Public functions
- **Examples**: Transaction validation, block validation, script execution

**Code**: [estimate_test_coverage.py](https://github.com/BTCDecoded/blvm-consensus/blob/main/estimate_test_coverage.py#L52-L94)

### Property-Based Tests

Property-based tests verify mathematical invariants:

- **Location**: `tests/consensus_property_tests.rs` and other property test files
- **Coverage**: Mathematical invariants
- **Tool**: Proptest

**Code**: [consensus_property_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/consensus_property_tests.rs#L1-L2025)

### Integration Tests

Integration tests verify end-to-end correctness:

- **Location**: `tests/integration/` directory
- **Coverage**: Multi-component scenarios
- **Examples**: BIP compliance, historical replay, mempool mining

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/mod.rs#L1-L35)

### Fuzz Tests

Fuzz tests discover edge cases through random generation:

- **Location**: `fuzz/fuzz_targets/` directory
- **Tool**: libFuzzer
- **Coverage**: Critical consensus functions

**Code**: [README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/fuzz/README.md#L1-L269)

### Formal Verification

[Formal verification](../consensus/formal-verification.md) verifies correctness for all inputs:

- **Location**: `src/` and `tests/` directories
- **Formal Verification**: Proofs with tiered execution system
- **Coverage**: Critical consensus functions
- **Tool**: Formal verification tooling

**Code**: [formal-verification.md](https://github.com/BTCDecoded/blvm-docs/blob/main/src/consensus/formal-verification.md#L1-L412)

### Z3 Proof Verification

BLVM Specification Lock provides formal verification of UTXO set operations:

- **Location**: `blvm-node/src/storage/utxostore_proofs.rs`
- **Coverage**: UTXO uniqueness, add/remove consistency, value conservation, round-trip storage
- **Tool**: BLVM Specification Lock (uses Z3 SMT solver)
- **Mathematical Specifications**: Verifies compliance with Orange Paper theorems

**Verified Properties**:
- UTXO uniqueness (Orange Paper Theorem 5.3.1)
- Add/remove consistency
- Spent output tracking
- Value conservation (Orange Paper Theorem 5.3.2)
- Count accuracy
- Round-trip storage (Orange Paper Theorem 5.3.3)

**Code**: [utxostore_proofs.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/utxostore_proofs.rs#L1-L229)

**See Also**: [UTXO Commitments](../consensus/utxo-commitments.md#utxo-proof-verification) - Proof verification workflow

### Runtime Assertions

Runtime assertions catch violations during execution:

- **Coverage**: Critical paths with runtime assertions
- **Production**: Available via feature flag

**Code**: [CONSENSUS_COVERAGE_ASSESSMENT.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/CONSENSUS_COVERAGE_ASSESSMENT.md#L156-L160)

### MIRI Integration

MIRI detects undefined behavior:

- **CI Integration**: Automated undefined behavior detection
- **Coverage**: Property tests and critical unit tests
- **Tool**: MIRI interpreter

**Code**: [CONSENSUS_COVERAGE_ASSESSMENT.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/CONSENSUS_COVERAGE_ASSESSMENT.md#L167-L170)

## Coverage Statistics

### Overall Coverage

| Verification Technique | Status |
|----------------------|--------|
| **Formal Proofs** | ✅ Critical functions |
| **Property Tests** | ✅ All mathematical invariants |
| **Runtime Assertions** | ✅ All critical paths |
| **Fuzz Targets** | ✅ Edge case discovery |
| **MIRI Integration** | ✅ Undefined behavior detection |
| **Mathematical Specs** | ✅ Complete formal documentation |

**Code**: [CONSENSUS_COVERAGE_ASSESSMENT.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/CONSENSUS_COVERAGE_ASSESSMENT.md#L10-L21)

### Coverage by Consensus Area

Verification coverage includes all major consensus areas:

- **Economic Rules**: Formal proofs, property tests, runtime assertions, and fuzz targets
- **Proof of Work**: Formal proofs, property tests, runtime assertions, and fuzz targets
- **Transaction Validation**: Formal proofs, property tests, runtime assertions, and fuzz targets
- **Block Validation**: Formal proofs, property tests, runtime assertions, and fuzz targets
- **Script Execution**: Formal proofs, property tests, runtime assertions, and fuzz targets
- **Chain Reorganization**: Formal proofs, property tests, and runtime assertions
- **Cryptographic**: Formal proofs, property tests, and runtime assertions
- **Mempool**: Formal proofs, runtime assertions, and fuzz targets
- **SegWit**: Formal proofs, runtime assertions, and fuzz targets
- **Serialization**: Formal proofs, runtime assertions, and fuzz targets

**Code**: [EXACT_VERIFICATION_COUNTS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/EXACT_VERIFICATION_COUNTS.md#L271-L283)

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

# Fuzz tests
cargo +nightly fuzz run transaction_validation
```

### Run with MIRI

```bash
cargo +nightly miri test
```

### Run Z3 Proofs

```bash
# Run BLVM Specification Lock verification
cargo spec-lock verify

# Verify specific proof
cargo spec-lock verify --proof verify_utxo_uniqueness
```

**Code**: [formal-verification.md](https://github.com/BTCDecoded/blvm-docs/blob/main/src/consensus/formal-verification.md#L1-L412)

**Code**: [utxostore_proofs.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/utxostore_proofs.rs#L1-L229)

## Coverage Goals

### Target Coverage

- **Z3 Proofs**: All critical consensus functions
- **Property Tests**: All mathematical invariants
- **Fuzz Targets**: All critical validation paths
- **Runtime Assertions**: All critical code paths
- **Integration Tests**: All major workflows

### Current Status

All coverage goals met:
- ✅ Formal proofs covering all critical functions
- ✅ Property test functions covering all invariants
- ✅ Fuzz targets covering all critical paths
- ✅ Runtime assertions in all critical paths
- ✅ Comprehensive integration test suite

**Code**: [CONSENSUS_COVERAGE_ASSESSMENT.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/CONSENSUS_COVERAGE_ASSESSMENT.md#L179-L196)

## Test Organization

### Directory Structure

```
blvm-consensus/
├── src/                    # Source code with Z3 proofs
├── tests/
│   ├── consensus_property_tests.rs  # Main property tests
│   ├── integration/         # Integration tests
│   ├── unit/               # Unit tests
│   ├── fuzzing/            # Fuzzing helpers
│   └── verification/       # Verification tests
└── fuzz/
    └── fuzz_targets/        # Fuzz targets
```

**Code**: [](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/#L1-L200)

## Edge Case Coverage

### Beyond Proof Bounds

Edge cases beyond Z3 proof bounds are covered by:

1. **Property-Based Testing**: Random inputs of various sizes
2. **Mainnet Block Tests**: Real Bitcoin mainnet blocks
3. **Integration Tests**: Realistic scenarios
4. **Fuzz Testing**: Random generation

**Code**: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md#L101-L140)

## Differential Testing

### Bitcoin Core Comparison

Differential tests compare behavior with Bitcoin Core:

- **Location**: `tests/integration/differential_tests.rs`
- **Purpose**: Verify consistency with Bitcoin Core
- **Coverage**: Critical consensus functions

**Code**: [differential_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/integration/differential_tests.rs#L1-L200)

## CI Integration

### Automated Testing

All tests run in CI:

- **Unit Tests**: Required for merge
- **Property Tests**: Required for merge
- **Integration Tests**: Required for merge
- **Fuzz Tests**: Run on schedule
- **Z3 Proofs**: Run separately, not blocking
- **MIRI**: Run on property tests and critical unit tests

**Code**: [formal-verification.md](https://github.com/BTCDecoded/blvm-docs/blob/main/src/consensus/formal-verification.md#L1-L412)

## Test Metrics

- **Property Test Functions**: Multiple functions across all files
- **Runtime Assertions**: Multiple assertions (`assert!` and `debug_assert!`)
- **Fuzz Targets**: Multiple fuzz targets

**Code**: [EXACT_VERIFICATION_COUNTS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/EXACT_VERIFICATION_COUNTS.md#L253-L265)

## Components

The testing infrastructure includes:
- Unit tests for all public functions
- Property-based tests for mathematical invariants
- Integration tests for end-to-end scenarios
- Fuzz tests for edge case discovery
- Z3 proofs for formal verification
- Runtime assertions for execution-time checks
- MIRI integration for undefined behavior detection
- Differential tests for Bitcoin Core comparison

**Location**: `blvm-consensus/tests/`, `blvm-consensus/fuzz/`, `blvm-consensus/src/`

## See Also

- [Property-Based Testing](property-based-testing.md) - Verify mathematical invariants
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Differential Testing](differential-testing.md) - Compare with Bitcoin Core
- [Benchmarking](benchmarking.md) - Performance measurement
- [Snapshot Testing](snapshot-testing.md) - Output consistency verification
- [Formal Verification](../consensus/formal-verification.md) - BLVM Specification Lock verification
- [UTXO Commitments](../consensus/utxo-commitments.md#utxo-proof-verification) - Z3 proof verification for UTXO operations
- [Contributing](contributing.md) - Testing requirements for contributions
