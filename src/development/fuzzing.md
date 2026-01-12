# Fuzzing Infrastructure

## Overview

Bitcoin Commons implements fuzzing infrastructure using libFuzzer for automated bug discovery. The system includes 19 fuzz targets covering all critical consensus validation functions, with sanitizer support and corpus management.

## Fuzz Targets

### Core Consensus (Critical)

1. **transaction_validation** - Transaction parsing and validation
2. **block_validation** - Block validation and connection
3. **script_execution** - Script VM execution
4. **script_opcodes** - Individual opcode execution

### Advanced Features

5. **segwit_validation** - SegWit weight calculations and witness validation
6. **mempool_operations** - Mempool acceptance, RBF, standardness checks
7. **utxo_commitments** - UTXO commitment verification

### Infrastructure

8. **serialization** - Serialization/deserialization round-trips
9. **pow_validation** - Proof of Work validation and difficulty adjustment
10. **economic_validation** - Supply and fee calculations
11. **compact_block_reconstruction** - Compact block parsing
12. **differential_fuzzing** - Internal consistency testing
13. **block_header_validation** - Block header validation
14. **merkle_validation** - Merkle tree validation
15. **signature_verification** - Signature verification
16. **taproot_validation** - Taproot validation
17. **transaction_input_validation** - Transaction input validation
18. **transaction_output_validation** - Transaction output validation
19. **reorganization** - Chain reorganization handling

**Location**: `blvm-consensus/fuzz/fuzz_targets/`

## Quick Start

### Initialize Corpus

```bash
cd blvm-consensus/fuzz
./init_corpus.sh
```

This creates corpus directories and adds basic seed inputs for all targets.

### Run a Fuzzing Campaign

```bash
# Run single target (5 minutes)
cargo +nightly fuzz run transaction_validation

# Run with corpus
cargo +nightly fuzz run transaction_validation fuzz/corpus/transaction_validation

# Run all targets (24 hours each, background)
./run_campaigns.sh --background

# Run with test runner (parallel execution)
python3 test_runner.py fuzz/corpus/ --parallel
```

### Build with Sanitizers

```bash
# AddressSanitizer (ASAN)
./build_with_sanitizers.sh asan

# UndefinedBehaviorSanitizer (UBSAN)
./build_with_sanitizers.sh ubsan

# MemorySanitizer (MSAN)
./build_with_sanitizers.sh msan

# All sanitizers
./build_with_sanitizers.sh all
```

## libFuzzer Integration

### Primary Fuzzing Engine

libFuzzer is the primary fuzzing engine, providing:
- Coverage-guided fuzzing
- Automatic corpus management
- Crash reproduction
- Mutation-based input generation

### Fuzz Target Structure

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // Parse and validate input
    if let Ok(transaction) = parse_transaction(data) {
        // Test validation function
        let _ = validate_transaction(&transaction);
    }
});
```

**Location**: `blvm-consensus/fuzz/fuzz_targets/`

## Sanitizer Support

### AddressSanitizer (ASAN)

Detects memory errors:
- Use-after-free
- Buffer overflows
- Memory leaks
- Double-free

**Usage**:
```bash
RUSTFLAGS="-Zsanitizer=address" cargo +nightly fuzz run transaction_validation
```

### UndefinedBehaviorSanitizer (UBSAN)

Detects undefined behavior:
- Integer overflow
- Null pointer dereference
- Invalid shifts
- Type mismatches

**Usage**:
```bash
RUSTFLAGS="-Zsanitizer=undefined" cargo +nightly fuzz run transaction_validation
```

### MemorySanitizer (MSAN)

Detects uninitialized memory reads:
- Uninitialized stack reads
- Uninitialized heap reads
- Uninitialized memory in structs

**Usage**:
```bash
RUSTFLAGS="-Zsanitizer=memory" cargo +nightly fuzz run transaction_validation
```

## Corpus Management

### Corpus Structure

```
fuzz/corpus/
├── transaction_validation/
├── block_validation/
├── script_execution/
├── script_opcodes/
├── segwit_validation/
├── mempool_operations/
├── utxo_commitments/
├── serialization/
├── pow_validation/
├── economic_validation/
├── compact_block_reconstruction/
└── differential_fuzzing/
```

### Corpus Initialization

The `init_corpus.sh` script:
- Creates corpus directories for all targets
- Adds basic seed inputs
- Sets up corpus structure

**Code**: `blvm-consensus/fuzz/init_corpus.sh`

### Corpus Growth

Corpus grows automatically as libFuzzer discovers new code paths:
- Coverage-guided selection
- Mutation-based generation
- Automatic deduplication
- Persistent storage

## Test Runner

### Parallel Execution

The `test_runner.py` script provides:
- Parallel fuzzing across targets
- Corpus management
- Crash reproduction
- Sanitizer integration
- Progress tracking

**Usage**:
```bash
python3 test_runner.py fuzz/corpus/ --parallel
```

**Code**: `blvm-consensus/fuzz/test_runner.py`

### Sequential Execution

For debugging or resource-constrained environments:

```bash
python3 test_runner.py fuzz/corpus/ --sequential
```

## Differential Fuzzing

### Internal Consistency Testing

Differential fuzzing verifies internal consistency without relying on Bitcoin Core:

- Multiple implementations of same function
- Round-trip properties
- Invariant checking
- Cross-component validation

**Code**: `blvm-consensus/fuzz/fuzz_targets/differential_fuzzing.rs`

## CI Integration

### Continuous Fuzzing

Fuzzing runs in CI via GitHub Actions:
- Automated corpus updates
- Crash detection
- Sanitizer builds
- Coverage tracking

**Location**: `.github/workflows/fuzz.yml`

## Running Fuzzing Campaigns

### Short Verification (5 minutes each)

```bash
./run_campaigns.sh 300
```

### Full Campaigns (24 hours each)

```bash
./run_campaigns.sh --background
```

### Individual Target

```bash
cargo +nightly fuzz run transaction_validation -- -max_total_time=3600
```

**Code**: `blvm-consensus/fuzz/run_campaigns.sh`

## Crash Reproduction

### Reproducing Crashes

```bash
# Run with crash input
cargo +nightly fuzz run transaction_validation crash_inputs/crash-abc123

# Run with sanitizer for detailed error
RUSTFLAGS="-Zsanitizer=address" cargo +nightly fuzz run transaction_validation crash_inputs/crash-abc123
```

### Crash Analysis

Crashes are automatically:
- Saved to `fuzz/artifacts/`
- Tagged with target name
- Reproducible with exact input
- Analyzable with sanitizers

## Coverage Tracking

### Coverage Reports

Generate coverage reports:

```bash
cargo +nightly fuzz coverage transaction_validation
```

### Coverage Analysis

- Identify untested code paths
- Guide fuzzing improvements
- Measure fuzzing effectiveness
- Track coverage over time

## Best Practices

### Seed Inputs

Provide diverse seed inputs:
- Valid transactions/blocks
- Edge cases
- Boundary conditions
- Real-world examples

### Corpus Maintenance

- Regularly update corpus
- Remove redundant inputs
- Add interesting inputs manually
- Share corpus across runs

### Sanitizer Usage

- Run with ASAN regularly
- Use UBSAN for undefined behavior
- Use MSAN for uninitialized memory
- Combine sanitizers for comprehensive testing

## Components

The fuzzing infrastructure includes:
- 12 fuzz targets covering all critical functions
- libFuzzer integration
- Sanitizer support (ASAN, UBSAN, MSAN)
- Corpus management
- Test runner for automation
- Differential fuzzing
- CI integration

**Location**: `blvm-consensus/fuzz/`

## See Also

- [Testing Infrastructure](testing.md) - Overview of all testing techniques
- [Property-Based Testing](property-based-testing.md) - Verify invariants with random inputs
- [Differential Testing](differential-testing.md) - Compare with Bitcoin Core
- [Formal Verification](../consensus/formal-verification.md) - Kani model checking
- [Contributing](contributing.md) - Testing requirements for contributions
