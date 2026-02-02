# Introduction

Welcome to the BLVM (Bitcoin Low-Level Virtual Machine) documentation!

BLVM implements Bitcoin consensus rules directly from the [Orange Paper](reference/orange-paper.md), provides protocol abstraction for multiple Bitcoin variants, delivers a production-ready node with full P2P networking, includes a developer SDK for custom implementations, and enforces cryptographic governance for transparent development.

## What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is compiler-like infrastructure for Bitcoin implementations. Like LLVM transforms source code through optimization passes, BLVM transforms the [Orange Paper](reference/orange-paper.md) mathematical specification into optimized, production-ready code via [optimization passes](consensus/architecture.md#optimization-passes).

### Compiler-Like Architecture

Like a compiler transforms source code → IR → optimized machine code, BLVM transforms:

1. **[Orange Paper](reference/orange-paper.md)** - Mathematical specification (IR/intermediate representation)
2. **[blvm-spec-lock](https://github.com/BTCDecoded/blvm-spec-lock)** - Formal verification tooling linking code to Orange Paper specifications
3. **[Optimization Passes](consensus/architecture.md#optimization-passes)** - Transform spec into optimized code:
   - **Pass 2**: Constant Folding (pre-computed constants, constant propagation)
   - **Pass 3**: Memory Layout Optimization (cache-aligned structures, compact frames)
   - **Pass 5**: SIMD Vectorization (batch operations, parallel processing)
   - Bounds Check Optimization (using proven bounds)
   - Dead Code Elimination
   - Inlining Hints for hot functions
4. **[blvm-consensus](consensus/overview.md)** - Optimized implementation with [formal verification](consensus/formal-verification.md)
5. **[blvm-protocol](protocol/overview.md)** - Protocol abstraction for mainnet, testnet, regtest
6. **[blvm-node](node/overview.md)** - Full Bitcoin node with storage, networking, RPC
7. **[blvm-sdk](sdk/overview.md)** - Developer toolkit and [module composition](architecture/module-system.md)
8. **[Governance](governance/overview.md)** - Cryptographic governance enforcement

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

## Key Features

### Core Components

- **[blvm-consensus](consensus/overview.md)** - Pure mathematical implementation with formal verification, BIP integration (BIP30, BIP34, BIP66, BIP90, BIP147)
- **[blvm-protocol](protocol/overview.md)** - Protocol variants (mainnet, testnet, regtest) and network messages
- **[blvm-node](node/overview.md)** - Full Bitcoin node with RPC, storage, and [module system](architecture/module-system.md)
- **[blvm-sdk](sdk/overview.md)** - Governance primitives and CLI tools (blvm-keygen, blvm-sign, blvm-verify)
- **blvm-commons** - GitHub integration, OpenTimestamps, Nostr, cross-layer validation

### Module System

BLVM includes a process-isolated module system enabling optional features:

- **[blvm-lightning](modules/lightning.md)** - Lightning Network module (LDK implementation)
- **[blvm-mesh](modules/mesh.md)** - Mesh networking module
- **[blvm-governance](modules/governance.md)** - Governance integration module
- **[blvm-stratum-v2](modules/stratum-v2.md)** - Stratum V2 mining module

### Key Capabilities

BLVM includes comprehensive Bitcoin node functionality:

- **Module System**: Process-isolated modules with enhanced security and process isolation
- **RBF and Mempool Policies**: Configurable replacement-by-fee modes with 5 eviction strategies
- **Payment Processing**: CTV (CheckTemplateVerify) support for advanced payment flows
- **Advanced Indexing**: Address and value range indexing for efficient queries
- **Formal Verification**: Formal verification for critical proofs
- **Differential Testing**: Infrastructure for comparing against Bitcoin Core
- **FIBRE Protocol**: High-performance relay protocol support

## License

This documentation is licensed under the MIT License, same as the BLVM codebase.

