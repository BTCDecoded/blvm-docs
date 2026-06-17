# Introduction

BLVM (Bitcoin Low-Level Virtual Machine) implements Bitcoin consensus from the [Orange Paper](reference/orange-paper.md), provides protocol abstraction for multiple Bitcoin variants, a **reference** full node with P2P networking, a developer SDK, and cryptographic governance for transparent development.

## Who is this for?

**Running a Bitcoin node?** [Operator guide](getting-started/operator-guide.md) — [Installation](getting-started/installation.md), [Quick Start](getting-started/quick-start.md), [Mainnet initial sync](getting-started/mainnet-sync.md). Read [Deployment posture](security/deployment-posture.md) before exposing RPC on mainnet.

**Building a module or integrating with the SDK?** [Developer guide](getting-started/developer-guide.md) — [Building your first module](getting-started/first-module.md), then [Building modules](sdk/module-development.md).

**Studying the spec or contributing to consensus?** The [Orange Paper](reference/orange-paper.md) is the normative spec. [Formal Verification](consensus/formal-verification.md) explains verification. Contributors: [Repository layout](development/repository-architecture.md), [Contributing](development/contributing.md).

## What is BLVM?

BLVM is compiler-like infrastructure for Bitcoin implementations. The [Orange Paper](reference/orange-paper.md) is the mathematical specification (IR). **blvm-consensus** implements those rules; [BLVM Specification Lock](https://github.com/BTCDecoded/blvm-spec-lock) and tests check the code against the spec. See [compiler-like architecture](reference/glossary.md#compiler-like-architecture) in the glossary.

**Stack:**

- **[Orange Paper](reference/orange-paper.md)** – Mathematical specification (IR)
- **[blvm-spec-lock](https://github.com/BTCDecoded/blvm-spec-lock)** – Links code to spec; validates implementation against the IR
- **[blvm-consensus](consensus/overview.md)** – Consensus implementation with [formal verification](consensus/formal-verification.md)
- **[blvm-protocol](protocol/overview.md)** – Protocol abstraction (mainnet, testnet, regtest)
- **[blvm-node](node/overview.md)** – Full node (storage, networking, RPC, [modules](architecture/module-system.md))
- **[blvm-sdk](sdk/overview.md)** – Developer toolkit and module composition
- **[Governance](governance/overview.md)** – Cryptographic governance enforcement

**Why "LVM"?** Like LLVM’s shared compiler infrastructure, BLVM provides shared infrastructure for Bitcoin implementations—the Orange Paper is the reference spec; node and consensus code is validated against it.

## Documentation Structure

- **Operators:** [Operator guide](getting-started/operator-guide.md) — install, sync, RPC, security
- **Developers:** [Developer guide](getting-started/developer-guide.md) — modules, SDK, contributing
- **Architecture** – System design, module system, events
- **Layers** – Consensus, protocol, node (each with overview and detailed pages)
- **Developer SDK** – Module development, API reference, examples
- **Governance** – Model, configuration, procedures
- **Reference** – Specifications, [API Index](reference/api-index.md), glossary

Documentation is maintained in source repositories alongside code and is aggregated at [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org).

## Getting Help

Report bugs or request features via GitHub Issues, ask questions in GitHub Discussions, or report security issues to security@thebitcoincommons.org.
