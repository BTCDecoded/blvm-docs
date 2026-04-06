# Introduction

Welcome to the BLVM documentation.

BLVM (Bitcoin Low-Level Virtual Machine) implements Bitcoin consensus from the [Orange Paper](reference/orange-paper.md), provides protocol abstraction for multiple Bitcoin variants, a **reference** full node with P2P networking, a developer SDK, and cryptographic governance for transparent development.

## What is BLVM?

BLVM is compiler-like infrastructure for Bitcoin implementations. There is a mathematical specification (the [Orange Paper](reference/orange-paper.md), treated as an intermediate representation / IR) and an implementation. The implementation is **validated against** the spec using [BLVM Specification Lock](https://github.com/BTCDecoded/blvm-spec-lock) (formal verification with Z3)—it is not generated or transformed from the IR. Alternative implementations can target the same Orange Paper and tooling.

**Stack:**

- **[Orange Paper](reference/orange-paper.md)** – Mathematical specification (IR)
- **[blvm-spec-lock](https://github.com/BTCDecoded/blvm-spec-lock)** – Links code to spec; validates implementation against the IR
- **[blvm-consensus](consensus/overview.md)** – Consensus implementation with [formal verification](consensus/formal-verification.md)
- **[blvm-protocol](protocol/overview.md)** – Protocol abstraction (mainnet, testnet, regtest)
- **[blvm-node](node/overview.md)** – Full node (storage, networking, RPC, [modules](architecture/module-system.md))
- **[blvm-sdk](sdk/overview.md)** – Developer toolkit and module composition
- **[Governance](governance/overview.md)** – Cryptographic governance enforcement

**Why "LVM"?** Like LLVM’s infrastructure for compilers, BLVM provides shared infrastructure for Bitcoin implementations—with the spec as the reference and the implementation validated against it, not generated from it.

## Documentation Structure

- **Getting Started** – Installation, quick start, first node
- **Architecture** – System design, module system, events
- **Layers** – Consensus, protocol, node (each with overview and detailed pages)
- **Developer SDK** – Module development, API reference, examples
- **Governance** – Model, configuration, procedures
- **Reference** – Specifications, [API Index](reference/api-index.md), glossary

Documentation is maintained in source repositories alongside code and is aggregated at [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org).

## Getting Help

Report bugs or request features via GitHub Issues, ask questions in GitHub Discussions, or report security issues to security@btcdecoded.org.

## License

This documentation is licensed under the MIT License, same as the BLVM codebase.
