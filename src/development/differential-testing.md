# Differential Testing

## Overview

Bitcoin Commons implements differential testing to compare validation results with Bitcoin Core, providing empirical validation of consensus correctness. This ensures compatibility and catches consensus divergences.

**Location**: Differential testing is implemented in `blvm-bench` (separate repository), not in `bllvm-consensus`. The `bllvm-consensus` repository contains only a placeholder/skeleton implementation.

## Purpose

Differential testing serves to:

- **Verify Compatibility**: Ensure validation results match Bitcoin Core
- **Catch Divergences**: Detect consensus differences early
- **Empirical Validation**: Provide real-world validation testing
- **Automated Consistency**: Automated consistency checks

## Implementation Location

**Primary Implementation**: `blvm-bench` repository
- Full differential testing infrastructure
- Bitcoin Core RPC integration
- Regtest node management
- BIP-specific differential tests

**Skeleton Implementation**: `bllvm-consensus/tests/integration/differential_tests.rs`
- Skeleton implementation exists
- Full implementation is in `blvm-bench` repository
- Integration with `blvm-bench` is planned

**Code**: ```1:8:bllvm-consensus/tests/integration/differential_tests.rs``` (skeleton)

## Architecture

### Comparison Process

1. **Local Validation**: Validate transaction/block locally
2. **Core RPC Call**: Call Bitcoin Core RPC for validation
3. **Result Comparison**: Compare local and Core results
4. **Divergence Detection**: Report any divergences

**Code**: ```31:78:bllvm-consensus/tests/integration/differential_tests.rs```

### Bitcoin Core RPC Integration

Differential tests use Bitcoin Core RPC:

- **testmempoolaccept**: Transaction validation
- **submitblock**: Block validation
- **JSON-RPC 2.0**: Standard RPC protocol

**Code**: ```133:184:bllvm-consensus/tests/integration/differential_tests.rs```

## Transaction Validation Comparison

### Comparison Function

```rust
pub async fn compare_transaction_validation(
    tx: &Transaction,
    config: &CoreRpcConfig,
) -> Result<ComparisonResult>
```

**Process**:
1. Validate transaction locally using `check_transaction`
2. Serialize transaction to hex
3. Call Bitcoin Core's `testmempoolaccept` RPC
4. Compare validation results
5. Report divergence if results differ

**Code**: ```31:78:bllvm-consensus/tests/integration/differential_tests.rs```

## Block Validation Comparison

### Comparison Function

```rust
pub async fn compare_block_validation(
    block: &Block,
    config: &CoreRpcConfig,
) -> Result<ComparisonResult>
```

**Process**:
1. Validate block locally using `connect_block`
2. Serialize block to hex
3. Call Bitcoin Core's `submitblock` RPC
4. Compare validation results
5. Report divergence if results differ

**Code**: ```80:131:bllvm-consensus/tests/integration/differential_tests.rs```

## Configuration

### Core RPC Configuration

```rust
pub struct CoreRpcConfig {
    pub url: String,              // e.g., "http://127.0.0.1:8332"
    pub username: Option<String>, // RPC username
    pub password: Option<String>,  // RPC password
}
```

**Default**: `http://127.0.0.1:8332` (local Bitcoin Core)

**Code**: ```13:29:bllvm-consensus/tests/integration/differential_tests.rs```

## Differential Fuzzing

### Fuzz Target

Differential fuzzing compares internal consistency:

- **Serialization Round-Trips**: Ensures serialize→deserialize preserves properties
- **Validation Consistency**: Same transaction validates the same way after round-trip
- **Calculation Idempotency**: Weight calculations, economic calculations are deterministic
- **Cross-Validation**: Different code paths agree on validation results

**Code**: ```1:20:bllvm-consensus/fuzz/fuzz_targets/differential_fuzzing.rs```

### Internal Consistency

Differential fuzzing tests internal consistency within blvm-consensus:

- **No Bitcoin Core Dependency**: Tests blvm-consensus independently
- **Round-Trip Properties**: Serialization round-trips
- **Validation Consistency**: Validation consistency across code paths
- **Calculation Determinism**: Deterministic calculations

**Code**: ```227:239:bllvm-consensus/fuzz/README.md```

## Bitcoin Core Test Vectors

### Test Vector Integration

Bitcoin Core test vectors are integrated:

- **Transaction Vectors**: `tx_valid.json`, `tx_invalid.json`
- **Script Vectors**: `script_valid.json`, `script_invalid.json`
- **Block Vectors**: `block_valid.json`, `block_invalid.json`

**Code**: ```11:28:bllvm-consensus/tests/BLINDSPOT_COVERAGE_REPORT.md```

### Test Execution

Test vectors are executed:

- **Parsing**: Parse test vector JSON files
- **Validation**: Execute validation with test vectors
- **Pass/Fail Reporting**: Report test results
- **Graceful Handling**: Handle missing test data gracefully

**Code**: ```11:28:bllvm-consensus/tests/BLINDSPOT_COVERAGE_REPORT.md```

## Mainnet Block Tests

### Real Block Validation

Real Bitcoin mainnet blocks are used:

- **Genesis Block**: Genesis block validation
- **SegWit Activation**: SegWit activation block validation
- **Taproot Activation**: Taproot activation block validation
- **Historical Blocks**: Blocks from all consensus eras

**Code**: ```43:49:bllvm-consensus/tests/BLINDSPOT_COVERAGE_REPORT.md```

## Historical Consensus Tests

### Historical Validation

Historical consensus validation tests:

- **CVE-2012-2459**: Merkle tree duplicate hash test framework
- **Pre-SegWit**: Block validation (height < 481824)
- **Post-SegWit**: Block validation (height >= 481824)
- **Post-Taproot**: Block validation (height >= 709632)
- **Halving Points**: Historical block subsidy calculations
- **Difficulty Adjustment**: Historical difficulty adjustment tests

**Code**: ```29:41:bllvm-consensus/tests/BLINDSPOT_COVERAGE_REPORT.md```

## Usage

### Running Differential Tests

Differential tests are run from the `blvm-bench` repository:

```bash
cd blvm-bench
cargo test --features differential
```

Or run specific BIP differential tests:

```bash
cargo test --test bip_differential
```

### Prerequisites

- Bitcoin Core binary available (auto-discovered or via `CORE_PATH` environment variable)
- `blvm-bench` repository cloned
- Network connectivity for RPC calls (if using remote Core node)

**Note**: The placeholder in `bllvm-consensus` is not functional and should not be used.

## Interpretation

### Comparison Results

```rust
pub struct ComparisonResult {
    pub local_valid: bool,
    pub core_valid: bool,
    pub divergence: bool,
    pub divergence_reason: Option<String>,
}
```

**Code**: ```31:78:bllvm-consensus/tests/integration/differential_tests.rs```

### Divergence Handling

When divergence is detected:

- **Report**: Detailed divergence report
- **Investigation**: Investigate root cause
- **Fix**: Fix consensus bug if found
- **Verification**: Re-run tests to verify fix

## Automated Consistency Checks

### CI Integration

Differential tests can be integrated into CI:

- **On PRs**: Run differential tests on pull requests
- **On Schedule**: Regular scheduled runs
- **Divergence Detection**: Fail CI on divergence
- **Reporting**: Report divergences with details

## Benefits

1. **Compatibility**: Ensures compatibility with Bitcoin Core
2. **Early Detection**: Catches consensus divergences early
3. **Empirical Validation**: Real-world validation testing
4. **Automated**: Automated consistency checks
5. **Comprehensive**: Tests across all consensus eras

## Components

The differential testing system includes:
- Transaction validation comparison
- Block validation comparison
- Bitcoin Core RPC integration
- Differential fuzzing
- Bitcoin Core test vector integration
- Mainnet block tests
- Historical consensus tests

**Primary Location**: `blvm-bench` repository
- `blvm-bench/src/core_builder.rs` - Bitcoin Core binary detection
- `blvm-bench/src/regtest_node.rs` - Regtest node management
- `blvm-bench/src/core_rpc_client.rs` - RPC client wrapper
- `blvm-bench/src/differential.rs` - Comparison framework
- `blvm-bench/tests/integration/bip_differential.rs` - BIP-specific tests

**Placeholder Location**: `bllvm-consensus/tests/integration/differential_tests.rs` (skeleton, not fully implemented)

**Differential Fuzzing**: `bllvm-consensus/fuzz/fuzz_targets/differential_fuzzing.rs` (internal consistency testing, not Core comparison)

## See Also

- [Testing Infrastructure](testing.md) - Overview of all testing techniques
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Property-Based Testing](property-based-testing.md) - Verify invariants with random inputs
- [Formal Verification](../consensus/formal-verification.md) - Kani model checking
- [Contributing](contributing.md) - Testing requirements for contributions
