# Property-Based Testing

## Overview

Bitcoin Commons uses property-based testing with Proptest to verify mathematical invariants across thousands of random inputs. The system includes property tests in the main test file and property test functions across all test files.

## Property Test Categories

### Economic Rules

1. `prop_block_subsidy_halving_schedule` - Verifies subsidy halves every 210,000 blocks
2. `prop_total_supply_monotonic_bounded` - Verifies supply increases monotonically and is bounded
3. `prop_block_subsidy_non_negative_decreasing` - Verifies subsidy is non-negative and decreasing

### Proof of Work

4. `prop_pow_target_expansion_valid_range` - Verifies target expansion within valid range
5. `prop_target_expansion_deterministic` - Verifies target expansion is deterministic

### Transaction Validation

6. `prop_transaction_output_value_bounded` - Verifies output values are bounded
7. `prop_transaction_non_empty_inputs_outputs` - Verifies transactions have inputs and outputs
8. `prop_transaction_size_bounded` - Verifies transaction size is bounded
9. `prop_coinbase_script_sig_length` - Verifies coinbase script sig length limits
10. `prop_transaction_validation_deterministic` - Verifies validation is deterministic

### Script Execution

11. `prop_script_execution_deterministic` - Verifies script execution is deterministic
12. `prop_script_size_bounded` - Verifies script size is bounded
13. `prop_script_execution_performance_bounded` - Verifies script execution performance

### Performance

14. `prop_sha256_performance_bounded` - Verifies SHA256 performance
15. `prop_double_sha256_performance_bounded` - Verifies double SHA256 performance
16. `prop_transaction_validation_performance_bounded` - Verifies transaction validation performance
17. `prop_script_execution_performance_bounded` - Verifies script execution performance
18. `prop_block_subsidy_constant_time` - Verifies block subsidy calculation is constant-time
19. `prop_target_expansion_performance_bounded` - Verifies target expansion performance

### Deterministic Execution

20. `prop_transaction_validation_deterministic` - Verifies transaction validation determinism
21. `prop_block_subsidy_deterministic` - Verifies block subsidy determinism
22. `prop_total_supply_deterministic` - Verifies total supply determinism
23. `prop_target_expansion_deterministic` - Verifies target expansion determinism
24. `prop_fee_calculation_deterministic` - Verifies fee calculation determinism

### Integer Overflow Safety

25. `prop_fee_calculation_overflow_safety` - Verifies fee calculation overflow safety
26. `prop_output_value_overflow_safety` - Verifies output value overflow safety
27. `prop_total_supply_overflow_safety` - Verifies total supply overflow safety

### Temporal/State Transition

28. `prop_supply_never_decreases_across_blocks` - Verifies supply never decreases
29. `prop_reorganization_preserves_supply` - Verifies reorganization preserves supply
30. `prop_supply_matches_expected_across_blocks` - Verifies supply matches expected values

### Compositional Verification

31. `prop_connect_block_composition` - Verifies block connection composition
32. `prop_disconnect_connect_idempotency` - Verifies disconnect/connect idempotency

### SHA256 Correctness

33. `sha256_matches_reference` - Verifies SHA256 matches reference implementation
34. `double_sha256_matches_reference` - Verifies double SHA256 matches reference
35. `sha256_idempotent` - Verifies SHA256 idempotency
36. `sha256_deterministic` - Verifies SHA256 determinism
37. `sha256_output_length` - Verifies SHA256 output length
38. `double_sha256_output_length` - Verifies double SHA256 output length

**Location**: `blvm-consensus/tests/consensus_property_tests.rs`

## Proptest Integration

### Basic Usage

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn prop_function_invariant(input in strategy) {
        let result = function_under_test(input);
        prop_assert!(result.property_holds());
    }
}
```

### Strategy Generation

Proptest generates random inputs using strategies:

```rust
// Integer strategy
let height_strategy = 0u64..10_000_000;

// Vector strategy
let tx_strategy = prop::collection::vec(tx_strategy, 1..1000);

// Custom strategy
let block_strategy = (height_strategy, tx_strategy).prop_map(|(h, txs)| {
    Block::new(h, txs)
});
```

### Property Assertions

```rust
// Basic assertion
prop_assert!(condition);

// Assertion with message
prop_assert!(condition, "Property failed: {}", reason);

// Assertion with equality
prop_assert_eq!(actual, expected);
```

## Property Test Patterns

### Invariant Testing

Test that invariants hold across all inputs:

```rust
proptest! {
    #[test]
    fn prop_subsidy_non_negative(height in 0u64..10_000_000) {
        let subsidy = get_block_subsidy(height);
        prop_assert!(subsidy >= 0);
    }
}
```

### Round-Trip Properties

Test that operations are reversible:

```rust
proptest! {
    #[test]
    fn prop_serialization_round_trip(tx in tx_strategy()) {
        let serialized = serialize(&tx);
        let deserialized = deserialize(&serialized)?;
        prop_assert_eq!(tx, deserialized);
    }
}
```

### Determinism Properties

Test that functions are deterministic:

```rust
proptest! {
    #[test]
    fn prop_deterministic(input in input_strategy()) {
        let result1 = function(input.clone());
        let result2 = function(input);
        prop_assert_eq!(result1, result2);
    }
}
```

### Bounds Properties

Test that values stay within bounds:

```rust
proptest! {
    #[test]
    fn prop_value_bounded(value in 0i64..MAX_MONEY) {
        let result = process_value(value);
        prop_assert!(result >= 0 && result <= MAX_MONEY);
    }
}
```

## Additional Property Tests

### Comprehensive Property Tests

**Location**: `tests/unit/comprehensive_property_tests.rs`
- Multiple proptest! blocks covering comprehensive scenarios

### Script Opcode Property Tests

**Location**: `tests/unit/script_opcode_property_tests.rs`
- Multiple proptest! blocks for script opcode testing

### SegWit/Taproot Property Tests

**Location**: `tests/unit/segwit_taproot_property_tests.rs`
- Multiple proptest! blocks for SegWit and Taproot

### Edge Case Property Tests

Multiple files with edge case testing:
- `tests/unit/block_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/economic_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/reorganization_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/transaction_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/utxo_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/difficulty_edge_cases.rs`: Multiple proptest! blocks
- `tests/unit/mempool_edge_cases.rs`: Multiple proptest! blocks

### Cross-BIP Property Tests

**Location**: `tests/cross_bip_property_tests.rs`
- Multiple proptest! blocks for cross-BIP validation

## Statistics

- **Property Test Blocks**: Multiple proptest! blocks across all test files
- **Property Test Functions**: Multiple prop_* functions across all test files

## Running Property Tests

### Run All Property Tests

```bash
cargo test --test consensus_property_tests
```

### Run Specific Property Test

```bash
cargo test --test consensus_property_tests prop_block_subsidy_halving_schedule
```

### Run with Verbose Output

```bash
cargo test --test consensus_property_tests -- --nocapture
```

### Run with MIRI

```bash
cargo +nightly miri test --test consensus_property_tests
```

## Shrinking

Proptest automatically shrinks failing inputs to minimal examples:

1. **Initial Failure**: Large random input fails
2. **Shrinking**: Proptest reduces input size
3. **Minimal Example**: Smallest input that still fails
4. **Debugging**: Minimal example is easier to debug

## Configuration

### Test Cases

Default: 256 test cases per property test

```rust
proptest! {
    #![proptest_config(ProptestConfig::with_cases(1000))]
    #[test]
    fn prop_test(input in strategy) {
        // ...
    }
}
```

### Max Shrink Iterations

Default: 65536 shrink iterations

```rust
proptest! {
    #![proptest_config(ProptestConfig {
        max_shrink_iters: 10000,
        ..ProptestConfig::default()
    })]
    #[test]
    fn prop_test(input in strategy) {
        // ...
    }
}
```

## Integration with Formal Verification

Property tests complement Z3 proofs:

- **BLVM Specification Lock (Z3)**: Proves correctness for all inputs (bounded)
- **Property Tests**: Verifies invariants with random inputs (unbounded)
- **Combined**: Comprehensive verification coverage

## Components

The property-based testing system includes:
- Property tests in main test file
- Property test blocks across all files
- Property test functions
- Proptest integration
- Strategy generation
- Automatic shrinking
- MIRI integration

**Location**: `blvm-consensus/tests/consensus_property_tests.rs`, `blvm-consensus/tests/unit/`

## See Also

- [Testing Infrastructure](testing.md) - Overview of all testing techniques
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Differential Testing](differential-testing.md) - Compare with Bitcoin Core
- [Formal Verification](../consensus/formal-verification.md) - BLVM Specification Lock verification
- [Contributing](contributing.md) - Testing requirements for contributions
