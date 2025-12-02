# Introduction

Welcome to the BLVM (Bitcoin Low-Level Virtual Machine) documentation!

BLVM implements Bitcoin consensus rules directly from the [Orange Paper](reference/orange-paper.md), provides protocol abstraction for multiple Bitcoin variants, delivers a production-ready node with full P2P networking, includes a developer SDK for custom implementations, and enforces cryptographic governance for transparent development.

## What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is compiler-like infrastructure for Bitcoin implementations. Like LLVM transforms source code through optimization passes, BLVM transforms the [Orange Paper](reference/orange-paper.md) mathematical specification into optimized, production-ready code via [optimization passes](consensus/architecture.md#optimization-passes).

### Compiler-Like Architecture

Like a compiler transforms source code → IR → optimized machine code, BLVM transforms:

1. **[Orange Paper](reference/orange-paper.md)** - Mathematical specification (IR/intermediate representation)
2. **[Optimization Passes](consensus/architecture.md#optimization-passes)** - Transform spec into optimized code:
   - **Pass 2**: Constant Folding (pre-computed constants, constant propagation)
   - **Pass 3**: Memory Layout Optimization (cache-aligned structures, compact frames)
   - **Pass 5**: SIMD Vectorization (batch operations, parallel processing)
   - Bounds Check Optimization (using [Kani](consensus/formal-verification.md)-proven bounds)
   - Dead Code Elimination
   - Inlining Hints for hot functions
3. **[bllvm-consensus](consensus/overview.md)** - Optimized implementation with [formal verification](consensus/formal-verification.md)
4. **[bllvm-protocol](protocol/overview.md)** - Protocol abstraction for mainnet, testnet, regtest
5. **[bllvm-node](node/overview.md)** - Full Bitcoin node with storage, networking, RPC
6. **[bllvm-sdk](sdk/overview.md)** - Developer toolkit and [module composition](architecture/module-system.md)
7. **[Governance](governance/overview.md)** - Cryptographic governance enforcement

### Why "LLVM"?

Like LLVM's compiler infrastructure, BLVM provides Bitcoin implementation infrastructure with [optimization passes](consensus/architecture.md#optimization-passes). The [Orange Paper](reference/orange-paper.md) serves as the intermediate representation (IR) transformed into production-ready code, enabling safe alternative implementations while maintaining consensus correctness.

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

- **[bllvm-consensus](consensus/overview.md)** - BIP integration (BIP30, BIP34, BIP66, BIP90, BIP147)
- **[bllvm-protocol](protocol/overview.md)** - Protocol variants and network messages
- **[bllvm-node](node/overview.md)** - Full node with RPC and storage
- **[bllvm-sdk](sdk/overview.md)** - Governance primitives and CLI tools
- **bllvm-commons** - GitHub integration, OTS, Nostr, cross-layer validation

### Production Readiness

- **Core Functionality** - Major features implemented (see [Node Overview](node/overview.md))
- **Governance Activation** - Governance rules not enforced (Phase 1, see [Governance Overview](governance/overview.md))
- **Maintainer Keys** - Test keys in use (2 real, 5+ test keys)
- **Integration Tests** - Test suite (see [Testing Infrastructure](development/testing.md))
- **Differential Testing** - Infrastructure exists, RPC library integration pending (see [Differential Testing](development/differential-testing.md))

**Note**: System is functionally complete but not yet activated in production. See [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md) for detailed information.

## License

This documentation is licensed under the MIT License, same as the BLVM codebase.

