# Consensus Layer Overview

The consensus layer (`blvm-consensus`) provides a pure mathematical implementation of Bitcoin consensus rules from the [Orange Paper](../reference/orange-paper.md). All functions are deterministic, side-effect-free, and directly implement the mathematical specifications without interpretation.

## Architecture Position

Tier 2 of the 6-tier Bitcoin Commons architecture:

```
1. Orange Paper (mathematical foundation)
2. blvm-consensus (pure math implementation) ← THIS LAYER
3. blvm-protocol (Bitcoin abstraction)
4. blvm-node (full node implementation)
5. blvm-sdk (developer toolkit)
6. blvm-commons (governance enforcement)
```

## Core Functions

Implements major Bitcoin consensus functions from the [Orange Paper](../reference/orange-paper.md):

### Transaction Validation
- `CheckTransaction`: Transaction structure and limit validation
- `CheckTxInputs`: Input validation against UTXO set
- `EvalScript`: Script execution engine
- `VerifyScript`: Script verification with witness data

**Code**: [transaction.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/transaction.rs#L1-L200)

### Block Validation
- `ConnectBlock`: Block connection and validation
- `ApplyTransaction`: Transaction application to UTXO set
- `CheckProofOfWork`: Proof of work verification
- `ShouldReorganize`: Chain reorganization logic

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L1-L300)

### Economic Model
- `GetBlockSubsidy`: Block reward calculation with halving
- `TotalSupply`: Total supply computation
- `GetNextWorkRequired`: Difficulty adjustment calculation

**Code**: [economic.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/economic.rs#L1-L200)

### Mempool Protocol
- `AcceptToMemoryPool`: Transaction mempool validation
- `IsStandardTx`: Standard transaction checks
- `ReplacementChecks`: RBF (Replace-By-Fee) logic

**Code**: [mempool.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/mempool.rs#L1-L200)

### Mining Protocol
- `CreateNewBlock`: Block creation from mempool
- `MineBlock`: Block mining and nonce finding
- `GetBlockTemplate`: Block template generation

**Code**: [mining.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/mining.rs#L1-L200)

### Advanced Features
- **SegWit**: Witness data validation and weight calculation
- **Taproot**: P2TR output validation and key aggregation

**Code**: [segwit.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/segwit.rs#L1-L200)

## Design Principles

1. **Pure Functions**: All functions are deterministic and side-effect-free
2. **Mathematical Accuracy**: Direct implementation of [Orange Paper](../reference/orange-paper.md) specifications
3. **Optimization Passes**: LLVM-like [optimization passes](architecture.md#optimization-passes) transform specifications into optimized code
4. **Exact Version Pinning**: All consensus-critical dependencies pinned to exact versions
5. **Comprehensive Testing**: Extensive test coverage with [unit tests](../development/testing.md), [property-based tests](../development/property-based-testing.md), and [integration tests](../development/testing.md#integration-tests)
6. **No Consensus Rule Interpretation**: Only mathematical implementation
7. **Formal Verification**: [blvm-spec-lock model checking](formal-verification.md) and [property-based testing](../development/property-based-testing.md) ensure correctness

## Formal Verification

Implements mathematical verification of Bitcoin consensus rules:

### Recent Improvements
- **Strong Tier System**: Critical proofs prioritized with AWS spot instance integration
- **Spam Filtering**: Always available (removed feature gate dependency)
- **Parallel Proof Execution**: Tiered scheduling for efficient verification

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L1-L412)

### Verification Coverage

**Chain Selection**: `should_reorganize`, `calculate_chain_work` verified  
**Block Subsidy**: `get_block_subsidy` halving schedule verified  
**Proof of Work**: `check_proof_of_work`, target expansion verified  
**Transaction Validation**: `check_transaction` structure rules verified  
**Block Connection**: `connect_block` UTXO consistency verified  

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md#L1-L100)

## BIP Implementation

Critical Bitcoin Improvement Proposals (BIPs) implemented:

- **BIP30**: Duplicate coinbase prevention (integrated in `connect_block()`)
- **BIP34**: Block height in coinbase (integrated in `connect_block()`)  
- **BIP66**: Strict DER signatures (enforced via script verification)
- **BIP90**: Block version enforcement (integrated in `connect_block()`)
- **BIP147**: NULLDUMMY enforcement (enforced via script verification)

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L1-L200)

## Performance Optimizations

### Profile-Guided Optimization (PGO)

For maximum performance:

```bash
./scripts/pgo-build.sh
```

**Expected gain**: Significant performance improvement

### Optimization Passes

LLVM-like optimization passes transform Orange Paper specifications:

- **Constant Folding**: Compile-time constant evaluation
- **Memory Layout Optimization**: Cache-friendly data structures
- **SIMD Vectorization**: Parallel processing where applicable
- **Bounds Check Optimization**: Eliminate unnecessary checks
- **Dead Code Elimination**: Remove unused code paths

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations/mod.rs#L1-L100)

## Mathematical Lock

Implementation is mathematically locked to the Orange Paper:

**Chain of Trust**:
```
Orange Paper (Math Spec) → blvm-spec-lock Proof → Implementation → Bitcoin Consensus
```

Every function implements a mathematical specification, every critical function has a blvm-spec-lock proof, and all proofs reference Orange Paper sections.

## Dependencies

All consensus-critical dependencies are pinned to exact versions:

```toml
# Consensus-critical cryptography - EXACT VERSIONS
secp256k1 = "=0.28.2"
sha2 = "=0.10.9"
ripemd = "=0.1.3"
bitcoin_hashes = "=0.11.0"
```

**Code**: [Cargo.toml](https://github.com/BTCDecoded/blvm-consensus/blob/main/Cargo.toml#L1-L163)

## See Also

- [Consensus Architecture](architecture.md) - Consensus layer design
- [Formal Verification](formal-verification.md) - Verification methodology
- [Mathematical Correctness](mathematical-correctness.md) - Verification approach and coverage
- [UTXO Commitments](utxo-commitments.md) - UTXO commitment system
- [Orange Paper](../reference/orange-paper.md) - Mathematical foundation

