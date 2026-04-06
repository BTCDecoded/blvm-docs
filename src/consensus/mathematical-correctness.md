# Mathematical Correctness

The consensus layer uses the Orange Paper, **BLVM Specification Lock**, tests, and code review together. Proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md), [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md).

## Verification Approach

Our verification approach follows: **"Rust + Tests + Math Specs = Source of Truth"**

### Layer 1: Empirical Testing (Required, Must Pass)
- **Unit tests**: Broad coverage across consensus modules
- **[Property-based tests](../development/property-based-testing.md)**: Randomized testing with `proptest` to discover edge cases
- **Integration tests**: Cross-system validation between consensus components

### Layer 2: Symbolic Verification
- **[BLVM Specification Lock](formal-verification.md)**: Z3-backed proofs on spec-locked consensus functions
- **Mathematical specifications**: Formal documentation of consensus rules
- **State space exploration**: Paths checked under spec-lock contracts

### Layer 3: CI Enforcement
- **Automated testing**: Required for merge
- **BLVM Specification Lock**: Tiered runs; merge/release policy in [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)
- **OpenTimestamps audit logging**: Optional transparency for verification artifacts

## Primary verification areas

- **Chain selection**: `should_reorganize`, `calculate_chain_work`
- **Block subsidy**: `get_block_subsidy` halving schedule
- **Proof of work**: `check_proof_of_work`, target expansion
- **Transaction validation**: `check_transaction` structure rules
- **Block connection**: `connect_block`, UTXO consistency

## Protection coverage

Proof bounds and related limits upstream:

- **[PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)**
- **[VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)**

## See Also

- [Consensus Architecture](architecture.md) - Consensus layer design
- [Formal Verification](formal-verification.md) - Verification methodology and tools
- [Consensus Overview](overview.md) - Consensus layer introduction
- [Orange Paper](../reference/orange-paper.md) - Mathematical foundation

