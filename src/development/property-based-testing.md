# Property-Based Testing

## Overview

Bitcoin Commons uses property-based testing with Proptest to verify mathematical invariants across thousands of random inputs. The system includes property tests in the main test file and property test functions across all test files.

The property tests live in `blvm-consensus` `tests/consensus_property_tests.rs` and `tests/orange_paper_property_tests.rs`. Edge cases live in `tests/unit/block_edge_cases.rs`, `reorganization_edge_cases.rs`, `transaction_edge_cases.rs`, `utxo_edge_cases.rs`, `difficulty_edge_cases.rs`, and `mempool_edge_cases.rs`.

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

## Running Property Tests

### Run All Property Tests

```bash
cargo test --test consensus_property_tests
```

### Run Specific Property Test

```bash
cargo test --test consensus_property_tests prop_halving_interval_boundary
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

Property tests complement **BLVM Specification Lock** (Z3 proofs on spec-locked code):

- **Spec-lock**: Formal proofs tied to Orange Paper contracts
- **Proptest**: Randomized invariant sampling over strategies
- **Together**: Complementary layers; see [proof limitations](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)

## Components

The property-based testing system includes:
- Property tests in main test file
- Property test blocks across all files
- Property test functions
- Proptest integration
- Strategy generation
- Automatic shrinking
- MIRI integration


## Source

- [blvm-consensus/tests/consensus_property_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/consensus_property_tests.rs)
- [blvm-consensus/tests/unit/](https://github.com/BTCDecoded/blvm-consensus/tree/main/tests/unit/): script opcode, segwit/taproot property tests
- [blvm-consensus/tests/cross_bip_property_tests.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/cross_bip_property_tests.rs)
## See Also

- [Testing Infrastructure](testing.md) - Overview of all testing techniques
- [Fuzzing Infrastructure](testing.md#fuzzing) - Automated bug discovery
- [Differential Testing](differential-testing.md) - Cross-check vs Core (RPC, historical, full-chain)
- [Formal Verification](../consensus/formal-verification.md) - BLVM Specification Lock verification
- [Contributing](contributing.md) - Testing requirements for contributions
