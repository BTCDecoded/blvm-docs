# Introduction

Welcome to the BLLVM (Bitcoin Low-Level Virtual Machine) documentation!

BLLVM is a comprehensive Bitcoin implementation ecosystem providing direct mathematical implementation of Bitcoin consensus rules, protocol abstraction for multiple Bitcoin variants, production-ready node implementation with full P2P networking, developer SDK for building custom implementations, and cryptographic governance for transparent, accountable development.

## What is BLLVM?

BLLVM is a layered architecture that builds from mathematical foundations to full implementation:

1. **Orange Paper** - Mathematical specification of Bitcoin consensus
2. **bllvm-consensus** - Pure mathematical implementation of consensus rules
3. **bllvm-protocol** - Protocol abstraction for mainnet, testnet, and variants
4. **bllvm-node** - Full Bitcoin node with storage, networking, and RPC
5. **bllvm-sdk** - Developer toolkit and module composition framework
6. **Governance** - Cryptographic governance enforcement system

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

- ✅ Core infrastructure implemented
- ⚠️ Not yet activated in production
- 🔧 Test keys only (no real cryptographic enforcement)

See [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md) for detailed information.

## License

This documentation is licensed under the MIT License, same as the BLLVM codebase.

