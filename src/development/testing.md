# Testing Infrastructure

## Overview

Bitcoin Commons uses a multi-layered testing strategy combining [formal verification](../consensus/formal-verification.md), [property-based testing](property-based-testing.md), [fuzzing](fuzzing.md), integration tests, and runtime assertions. This approach ensures correctness across consensus-critical code.

## Testing Strategy

### Layered Verification

The testing strategy uses multiple complementary techniques:

1. **[Formal Verification](../consensus/formal-verification.md) (Kani)**: Proves correctness for all inputs (bounded)
2. **[Property-Based Testing](property-based-testing.md) (Proptest)**: Verifies invariants with random inputs (unbounded)
3. **[Fuzzing](fuzzing.md) (libFuzzer)**: Discovers edge cases through random generation
4. **Integration Tests**: Verifies end-to-end correctness
5. **Unit Tests**: Tests individual functions
6. **Runtime Assertions**: Catches violations during execution
7. **MIRI Integration**: Detects undefined behavior

**Code**: ```1:196:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

## Test Types

### Unit Tests

Unit tests verify individual functions in isolation:

- **Location**: `tests/` directory, `#[test]` functions
- **Coverage**: Public functions
- **Examples**: Transaction validation, block validation, script execution

**Code**: ```52:94:bllvm-consensus/estimate_test_coverage.py```

### Property-Based Tests

Property-based tests verify mathematical invariants:

- **Location**: `tests/consensus_property_tests.rs` and other property test files
- **Count**: 35 property tests in main file, 141 property test functions total
- **Coverage**: Mathematical invariants
- **Tool**: Proptest

**Code**: ```1:2025:bllvm-consensus/tests/consensus_property_tests.rs```

### Integration Tests

Integration tests verify end-to-end correctness:

- **Location**: `tests/integration/` directory
- **Coverage**: Multi-component scenarios
- **Examples**: BIP compliance, historical replay, mempool mining

**Code**: ```1:35:bllvm-consensus/tests/integration/mod.rs```

### Fuzz Tests

Fuzz tests discover edge cases through random generation:

- **Location**: `fuzz/fuzz_targets/` directory
- **Count**: 13 fuzz targets
- **Tool**: libFuzzer
- **Coverage**: Critical consensus functions

**Code**: ```1:269:bllvm-consensus/fuzz/README.md```

### Formal Verification (Kani)

[Kani proofs](../consensus/formal-verification.md) verify correctness for all inputs:

- **Location**: `src/` and `tests/` directories
- **Count**: 201 proofs in `src/`, 9 in `tests/` (210 total)
- **Coverage**: Critical consensus functions
- **Tool**: Kani model checker

**Code**: ```1:412:bllvm-docs/src/consensus/formal-verification.md```

### Runtime Assertions

Runtime assertions catch violations during execution:

- **Count**: 913 total assertions (99 `debug_assert!` + 814 `assert!`)
- **Coverage**: Critical paths
- **Production**: Available via feature flag

**Code**: ```156:160:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

### MIRI Integration

MIRI detects undefined behavior:

- **CI Integration**: Automated undefined behavior detection
- **Coverage**: Property tests and critical unit tests
- **Tool**: MIRI interpreter

**Code**: ```167:170:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

## Coverage Statistics

### Overall Coverage

| Verification Technique | Count | Status |
|----------------------|-------|--------|
| **Kani Formal Proofs** | **201** (210 total) | ✅ Critical functions |
| **Property Tests** | **35** (141 functions) | ✅ All mathematical invariants |
| **Runtime Assertions** | **913** | ✅ All critical paths |
| **Fuzz Targets** | **13** | ✅ Edge case discovery |
| **MIRI Integration** | ✅ | ✅ Undefined behavior detection |
| **Mathematical Specs** | **15+** | ✅ Complete formal documentation |

**Code**: ```10:21:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

### Coverage by Consensus Area

| Area | Kani Proofs | Property Tests | Runtime Assertions | Fuzz Targets |
|------|-------------|----------------|-------------------|--------------|
| Economic Rules | 8 | 3 | 53 | 1 |
| Proof of Work | 11 | 2 | 69 | 1 |
| Transaction Validation | 19 | 5 | 77 | 1 |
| Block Validation | 19 | 2 | 73 | 1 |
| Script Execution | 23 | 3 | 145 | 2 |
| Chain Reorganization | 6 | 2 | 28 | - |
| Cryptographic | 4 | 6 | 3 | - |
| Mempool | 12 | - | 58 | 1 |
| SegWit | 13 | - | 42 | 1 |
| Serialization | 4 | - | 30 | 1 |

**Code**: ```271:283:bllvm-consensus/docs/EXACT_VERIFICATION_COUNTS.md```

## Running Tests

### Run All Tests

```bash
cd bllvm-consensus
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

### Run Kani Proofs

```bash
cargo kani
```

**Code**: ```1:412:bllvm-docs/src/consensus/formal-verification.md```

## Coverage Goals

### Target Coverage

- **Kani Proofs**: All critical consensus functions
- **Property Tests**: All mathematical invariants
- **Fuzz Targets**: All critical validation paths
- **Runtime Assertions**: All critical code paths
- **Integration Tests**: All major workflows

### Current Status

All coverage goals met:
- ✅ 201 Kani proofs covering all critical functions
- ✅ 141 property test functions covering all invariants
- ✅ 13 fuzz targets covering all critical paths
- ✅ 913 runtime assertions in all critical paths
- ✅ Comprehensive integration test suite

**Code**: ```179:196:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

## Test Organization

### Directory Structure

```
bllvm-consensus/
├── src/                    # Source code with Kani proofs
├── tests/
│   ├── consensus_property_tests.rs  # Main property tests
│   ├── integration/         # Integration tests
│   ├── unit/               # Unit tests
│   ├── fuzzing/            # Fuzzing helpers
│   └── verification/       # Verification tests
└── fuzz/
    └── fuzz_targets/        # Fuzz targets
```

**Code**: ```1:200:bllvm-consensus/tests/```

## Edge Case Coverage

### Beyond Proof Bounds

Edge cases beyond Kani proof bounds are covered by:

1. **Property-Based Testing**: Random inputs of various sizes
2. **Mainnet Block Tests**: Real Bitcoin mainnet blocks
3. **Integration Tests**: Realistic scenarios
4. **Fuzz Testing**: Random generation

**Code**: ```101:140:bllvm-consensus/docs/PROOF_LIMITATIONS.md```

## Differential Testing

### Bitcoin Core Comparison

Differential tests compare behavior with Bitcoin Core:

- **Location**: `tests/integration/differential_tests.rs`
- **Purpose**: Verify consistency with Bitcoin Core
- **Coverage**: Critical consensus functions

**Code**: ```1:200:bllvm-consensus/tests/integration/differential_tests.rs```

## CI Integration

### Automated Testing

All tests run in CI:

- **Unit Tests**: Required for merge
- **Property Tests**: Required for merge
- **Integration Tests**: Required for merge
- **Fuzz Tests**: Run on schedule
- **Kani Proofs**: Run separately, not blocking
- **MIRI**: Run on property tests and critical unit tests

**Code**: ```1:412:bllvm-docs/src/consensus/formal-verification.md```

## Test Metrics

### Verification Counts

- **Kani Proofs**: 201 in `src/`, 9 in `tests/` (210 total)
- **Property Test Blocks**: 125 across all files
- **Property Test Functions**: 141 across all files
- **Runtime Assertions**: 913 total (814 `assert!` + 99 `debug_assert!`)
- **Fuzz Targets**: 13

**Code**: ```253:265:bllvm-consensus/docs/EXACT_VERIFICATION_COUNTS.md```

## Components

The testing infrastructure includes:
- Unit tests for all public functions
- Property-based tests for mathematical invariants
- Integration tests for end-to-end scenarios
- Fuzz tests for edge case discovery
- Kani proofs for formal verification
- Runtime assertions for execution-time checks
- MIRI integration for undefined behavior detection
- Differential tests for Bitcoin Core comparison

**Location**: `bllvm-consensus/tests/`, `bllvm-consensus/fuzz/`, `bllvm-consensus/src/`

## See Also

- [Property-Based Testing](property-based-testing.md) - Verify mathematical invariants
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Differential Testing](differential-testing.md) - Compare with Bitcoin Core
- [Benchmarking](benchmarking.md) - Performance measurement
- [Snapshot Testing](snapshot-testing.md) - Output consistency verification
- [Formal Verification](../consensus/formal-verification.md) - Kani model checking
- [Contributing](contributing.md) - Testing requirements for contributions
