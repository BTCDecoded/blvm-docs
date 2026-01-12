# Consensus Layer Architecture

The consensus layer is designed as a pure mathematical implementation with no side effects.

## Design Principles

1. **Pure Functions**: All functions are deterministic and side-effect-free
2. **Mathematical Accuracy**: Direct implementation of [Orange Paper](../reference/orange-paper.md) specifications
3. **Optimization Passes**: LLVM-like optimization passes transform the [Orange Paper](../reference/orange-paper.md) specification into optimized code (constant folding, memory layout optimization, SIMD vectorization, bounds check optimization, dead code elimination)
4. **Exact Version Pinning**: All consensus-critical dependencies pinned to exact versions
5. **Testing**: Test coverage with [unit tests](../development/testing.md), [property-based tests](../development/property-based-testing.md), and [integration tests](../development/testing.md#integration-tests)
6. **No Consensus Rule Interpretation**: Only mathematical implementation
7. **Formal Verification**: [Kani model checking](formal-verification.md) and [property-based testing](../development/property-based-testing.md) ensure correctness

## Core Functions

### Transaction Validation
- Transaction structure and limit validation
- Input validation against UTXO set
- [Script execution](overview.md#transaction-validation) and verification

### Block Validation
- [Block connection](overview.md#block-validation) and validation
- Transaction application to UTXO set
- [Proof of work verification](overview.md#block-validation)

### Economic Model
- Block reward calculation
- Total supply computation
- Difficulty adjustment

### Mempool Protocol
- Transaction mempool validation
- Standard transaction checks
- Transaction replacement (RBF) logic

### Mining Protocol
- Block creation from mempool
- Block mining and nonce finding
- Block template generation

### Chain Management
- Chain reorganization handling
- P2P network message processing

### Advanced Features
- **SegWit**: Witness data validation and weight calculation (see [BIP141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki))
- **Taproot**: P2TR output validation and key aggregation (see [BIP341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki))

## Optimization Passes

BLVM includes LLVM-like optimization passes that transform the Orange Paper specification into optimized, production-ready code:

- **Pass 2: Constant Folding** - Pre-computed constants and constant propagation to avoid runtime computation in hot paths
- **Pass 3: Memory Layout Optimization** - Cache-aligned structures (32-byte alignment) and compact stack frames for better cache performance
- **Pass 5: SIMD Vectorization** - Batch hash operations (SHA256, double SHA256, RIPEMD160, HASH160) with parallel processing using Rayon
- **Bounds Check Optimization** - Uses [Kani](formal-verification.md)-proven bounds to remove redundant runtime bounds checks
- **Dead Code Elimination** - Markers for unused code paths that can be eliminated
- **Inlining Hints** - `hot_inline!` macro for aggressive inlining of hot functions

These optimization passes are similar to LLVM's optimization infrastructure, transforming the mathematical specification ([Orange Paper](../reference/orange-paper.md)) into optimized code while maintaining correctness through [formal verification](formal-verification.md).

## Mathematical Protections

{{#include ../../../modules/blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md}}

## Spec Maintenance Workflow

![Spec Maintenance Workflow](../images/spec-maintenance-workflow.png)
*Figure: Specification maintenance workflow showing how changes are detected, verified, and integrated.*

## See Also

- [Consensus Overview](overview.md) - Consensus layer introduction
- [Formal Verification](formal-verification.md) - Verification methodology and tools
- [Mathematical Correctness](mathematical-correctness.md) - Verification approach and coverage
- [Orange Paper](../reference/orange-paper.md) - Mathematical foundation
- [Protocol Architecture](../protocol/architecture.md) - Protocol layer built on consensus

