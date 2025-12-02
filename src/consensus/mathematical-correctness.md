# Mathematical Correctness

The consensus layer implements mathematical correctness through formal verification and comprehensive testing.

## Verification Approach

Our verification approach follows: **"Rust + Tests + Math Specs = Source of Truth"**

### Layer 1: Empirical Testing (Required, Must Pass)
- **Unit tests**: Comprehensive test coverage for all consensus functions
- **[Property-based tests](../development/property-based-testing.md)**: Randomized testing with `proptest` to discover edge cases
- **Integration tests**: Cross-system validation between consensus components

### Layer 2: Symbolic Verification (Required, Must Pass)
- **[Kani model checking](formal-verification.md)**: Bounded symbolic verification with mathematical invariants
- **Mathematical specifications**: Formal documentation of consensus rules
- **State space exploration**: Verification of all possible execution paths

### Layer 3: CI Enforcement (Required, Blocks Merge)
- **Automated verification**: All tests and proofs must pass before merge
- **OpenTimestamps audit logging**: Immutable proof of verification artifacts
- **No human override**: Technical correctness is non-negotiable

## Verified Functions

✅ **Chain Selection**: `should_reorganize`, `calculate_chain_work` verified  
✅ **Block Subsidy**: `get_block_subsidy` halving schedule verified  
✅ **Proof of Work**: `check_proof_of_work`, target expansion verified  
✅ **Transaction Validation**: `check_transaction` structure rules verified  
✅ **Block Connection**: `connect_block` UTXO consistency verified  

## Protection Coverage

{{#include ../../../modules/bllvm-consensus/docs/PROTECTION_COVERAGE.md}}

## See Also

- [Consensus Architecture](architecture.md) - Consensus layer design
- [Formal Verification](formal-verification.md) - Verification methodology and tools
- [Consensus Overview](overview.md) - Consensus layer introduction
- [Orange Paper](../reference/orange-paper.md) - Mathematical foundation

