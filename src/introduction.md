# Introduction

Welcome to the BLLVM (Bitcoin Low-Level Virtual Machine) documentation!

BLLVM is a comprehensive Bitcoin implementation ecosystem providing direct mathematical implementation of Bitcoin consensus rules, protocol abstraction for multiple Bitcoin variants, production-ready node implementation with full P2P networking, developer SDK for building custom implementations, and cryptographic governance for transparent, accountable development.

## What is BLLVM?

BLLVM (Bitcoin Low-Level Virtual Machine) is a compiler-like infrastructure for Bitcoin implementations, similar to how LLVM provides compiler infrastructure for programming languages. BLLVM transforms mathematical specifications into optimized, production-ready code through a series of optimization passes.

### Compiler-Like Architecture

Like a compiler transforms source code → IR → optimized machine code, BLLVM transforms:

1. **Orange Paper** - Mathematical specification (acts as IR/intermediate representation)
2. **Optimization Passes** - Runtime optimization passes that transform the spec into optimized code:
   - **Pass 2**: Constant Folding (pre-computed constants, constant propagation)
   - **Pass 3**: Memory Layout Optimization (cache-aligned structures, compact frames)
   - **Pass 5**: SIMD Vectorization (batch operations, parallel processing)
   - Bounds Check Optimization (using Kani-proven bounds)
   - Dead Code Elimination
   - Inlining Hints for hot functions
3. **bllvm-consensus** - Optimized mathematical implementation with formal verification
4. **bllvm-protocol** - Protocol abstraction for mainnet, testnet, and variants
5. **bllvm-node** - Full Bitcoin node with storage, networking, and RPC
6. **bllvm-sdk** - Developer toolkit and module composition framework
7. **Governance** - Cryptographic governance enforcement system

### Why "LLVM"?

Just as LLVM provides compiler infrastructure with optimization passes, BLLVM provides Bitcoin implementation infrastructure with optimization passes. The Orange Paper serves as the intermediate representation (IR) that gets transformed through optimization passes into production-ready code, enabling safe alternative implementations while maintaining consensus correctness.

## Documentation Structure

This documentation is organized into several sections:

- **Getting Started** - Installation and quick start guides
- **Architecture** - System-wide design and component relationships
- **Component Documentation** - Detailed documentation for each layer
- **Developer Guides** - SDK usage and module development
- **Governance** - Governance model and procedures
- **Reference** - Specifications, API documentation, and glossary

## Documentation Sources

This unified documentation site aggregates content from multiple source repositories:

- Documentation is maintained in source repositories alongside code
- Changes to source documentation automatically propagate here
- Each component's documentation is authored by its maintainers

## Getting Help

Report bugs or request features on GitHub Issues, ask questions in GitHub Discussions, or report security issues to security@btcdecoded.org.

## Status

⚠️ **Current Status**: Phase 1 (Infrastructure Building)

### Core Components

- **bllvm-consensus** - BIP integration (BIP30, BIP34, BIP66, BIP90, BIP147)
- **bllvm-protocol** - Protocol variants and network messages
- **bllvm-node** - Full node with RPC and storage
- **bllvm-sdk** - Governance primitives and CLI tools
- **bllvm-commons** - GitHub integration, OTS, Nostr, cross-layer validation

### Production Readiness

- **Core Functionality** - All major features
- **Governance Activation** - Governance rules not enforced (Phase 1)
- **Maintainer Keys** - Test keys in use (2 real, 5+ test keys)
- **Integration Tests** - Comprehensive test suite
- **Differential Testing** - Infrastructure exists, RPC library integration pending

**Note**: System is functionally complete but not yet activated in production. See [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md) for detailed information.

## License

This documentation is licensed under the MIT License, same as the BLLVM codebase.

