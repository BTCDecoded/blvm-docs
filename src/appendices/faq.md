# Frequently Asked Questions

## General Questions

### What is Bitcoin Commons?

Bitcoin Commons is a project that solves Bitcoin's governance asymmetry through two complementary innovations: [BLVM](../introduction.md) (the technical stack providing mathematical rigor) and Bitcoin Commons (the governance framework providing coordination without civil war). Together, they enable safe alternative Bitcoin implementations with forkable governance. See [Introduction](../introduction.md) and [Governance Overview](../governance/overview.md) for details.

### How does this relate to other Bitcoin implementations?

The widely deployed reference stack is one mature codebase and informal governance. Bitcoin Commons adds: (1) BLVM — mathematical rigor and a normative Orange Paper, (2) Commons — forkable governance. The goals are implementation diversity and verifiable specs alongside strong consensus testing.

### Is this a fork of Bitcoin?

No. Neither BLVM nor Bitcoin Commons forks Bitcoin's blockchain or consensus rules. BLVM provides mathematical specification enabling safe alternative implementations. Bitcoin Commons provides governance framework enabling coordination. Both maintain full Bitcoin consensus compatibility.

### Is the system production ready?

BLVM provides a complete node implementation with core components, formal verification tooling, and broad tests. **Readiness depends on your deployment**: governance is not universally activated, and you must apply your own security review, hardening, RPC authentication, and monitoring. See [Node Configuration](../node/configuration.md), [Security](../security/security-controls.md), and [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md).

### How do BLVM and Bitcoin Commons work together?

BLVM provides the mathematical foundation and compiler-like architecture (Orange Paper as spec/IR; implementation validated against it). Bitcoin Commons provides the governance framework (coordination without civil war). The modular architecture is where both meet: BLVM supplies the spec and verification stack; Commons supplies governance. Production deployments need engineering and operations like any node.

### What are the two innovations?

**BLVM (Bitcoin Low-Level Virtual Machine)**: Technical innovation combining the [Orange Paper](../reference/orange-paper.md) (normative math spec), [formal verification](../consensus/formal-verification.md) (**BLVM Specification Lock** / Z3), and a compiler-like split between spec and implementation. See [Introduction](../introduction.md) and [Consensus Overview](../consensus/overview.md).

**Bitcoin Commons (Cryptographic Commons)**: Governance innovation providing forkable governance through Ostrom's principles, cryptographic enforcement, [5-tier governance model](../governance/layer-tier-model.md), and [transparent audit trails](../governance/audit-trails.md). This ensures coordination. See [Governance Overview](../governance/overview.md) for details.

### What's the relationship between Bitcoin Commons and BTCDecoded?

Bitcoin Commons is the governance framework; BTCDecoded is the first complete implementation of both innovations (BLVM + Commons). Think of BLVM as the technical foundation, Bitcoin Commons as the governance constitution, and BTCDecoded as the first "government" built on both. Other implementations can adopt the same framework.

### What is Bitcoin Commons (the governance framework)?

Bitcoin Commons is a forkable governance framework that applies Elinor Ostrom's proven commons management principles through cryptographic enforcement. It solves Bitcoin's governance asymmetry by making development governance as robust as technical consensus. It provides coordination without civil war through forkable rules, cryptographic signatures, and transparent audit trails.

### How does Bitcoin Commons governance work?

Bitcoin Commons uses a 5-tier constitutional governance model with graduated signature thresholds (3-of-5 for routine maintenance, up to 6-of-7 for consensus changes) and review periods (7 days to 365 days). All governance actions are cryptographically signed and transparently auditable. Users can fork governance rules if they disagree, creating exit competition.

### What makes Bitcoin Commons governance "6x harder to capture"?

Multiple mechanisms: (1) Forkable governance rules allow users to exit if governance is captured, (2) Multiple implementations compete, preventing monopoly, (3) Cryptographic enforcement makes power visible and accountable, (4) Economic alignment through merge mining, (5) Graduated thresholds prevent rapid changes, (6) Transparent audit trails.

### How does forkable governance work?

Users can fork the governance rules (not just the code) if they disagree with decisions. This creates exit competition: if governance is captured, users can fork to a better governance model while maintaining Bitcoin consensus compatibility. The threat of forking prevents capture.

### What are Ostrom's principles?

Elinor Ostrom's Nobel Prize-winning research identified 8 principles for managing commons successfully. Bitcoin Commons applies these through: clearly defined boundaries, proportional equivalence, collective choice, monitoring, graduated sanctions, conflict resolution, minimal recognition of rights, and nested enterprises.

### Why do you need both BLVM and Bitcoin Commons?

BLVM addresses the technical problem (shared Orange Paper spec, layered verification, alternative implementations). Bitcoin Commons addresses the governance problem (coordination without civil war). They are designed to work together.

### How does the modular architecture combine both innovations?

The modular architecture has three layers: (1) **Mandatory Consensus** (shared **blvm-consensus** rules and verification policy), (2) **Optional Modules** (Commons enables competition), (3) **Economic Coordination** (module marketplace funds infrastructure). Consensus stays in one layer; Commons coordinates changes and releases. The architecture is where both meet.

### Can you use BLVM without Bitcoin Commons governance?

Yes. BLVM is a technical stack usable on its own. Without Bitcoin Commons governance you do not get this project’s governance model. BLVM supplies the spec and implementation stack; Commons supplies coordination between alternatives.

### Can you use Bitcoin Commons governance without BLVM?

The governance framework can apply to other implementations. BLVM’s Orange Paper and verification stack give a shared spec and Z3-backed proofs on spec-locked code; any codebase still needs correct implementation and review to stay aligned with mainnet.

### What happens if governance is captured?

Forkable governance means users can fork to a better governance model. This creates exit competition: captured governance loses users to better-governed implementations. The threat of forking prevents capture. Here you can fork **governance rules**, not only application code.

### How does economic alignment work?

Through the module marketplace. Module authors receive 75% of sales, Commons receives 15% for infrastructure, and node operators receive 10%. This creates sustainable funding while incentivizing quality module development.

### What is merge mining?

Merge mining is available as a separate paid plugin module (`blvm-merge-mining`). It allows miners to mine multiple blockchains simultaneously using the same proof-of-work. However, merge mining is not a Commons funding model - revenue goes to the module developer, not to Commons infrastructure.

### What features does BLVM provide?

The Orange Paper, blvm-consensus (with formal verification tooling), blvm-protocol, blvm-node, blvm-sdk, and blvm-commons (governance enforcement) exist as implemented layers. **Governance rules are not yet activated in production**; treat the stack as experimental until your deployment’s activation criteria are met. See [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md) and [Governance Overview](../governance/overview.md).

### How is Bitcoin Commons governance implemented?

Bitcoin Commons governance uses a 5-tier constitutional model with cryptographic enforcement. Governance rules are defined, the governance-app is implemented, and cryptographic primitives are available. Governance activation requires a suitable cohort of keyholders to be onboarded. See [Governance Overview](../governance/overview.md) for details.

### How does governance activation work?

Governance activation requires a suitable cohort of keyholders to be onboarded. This involves security audits, keyholder onboarding, governance app deployment, and community testing. See [Governance Overview](../governance/overview.md) and [Keyholder Procedures](../governance/keyholder-procedures.md) for details.

### How can I contribute?

Review BLVM code and formal proofs, review Bitcoin Commons governance rules, submit issues and pull requests, help with testing and security audits, build your own implementation using both innovations, or participate in governance discussions.

### Can I build my own implementation?

Yes! You can use BLVM's technical stack (Orange Paper, blvm-consensus) and adopt Bitcoin Commons governance framework. Fork the governance model, customize it for your organization, and build your own Bitcoin-compatible implementation. See the [Implementations Registry](https://github.com/BTCDecoded/governance/blob/main/IMPLEMENTATIONS_REGISTRY.md).

### Where is the code?

All code is open source on GitHub under the [BTCDecoded organization](https://github.com/BTCDecoded). Key repositories: BLVM (blvm-spec/Orange Paper, blvm-consensus, blvm-protocol, blvm-node, blvm-sdk) and Commons (governance, governance-app).

### What documentation should I read?

[White Paper](https://thebitcoincommons.org/whitepaper.html) for complete technical and governance overview, [Unified Documentation](https://docs.thebitcoincommons.org) for technical documentation, and [Governance Docs](https://github.com/BTCDecoded/governance) for governance rules and processes.

### Why "commons"?

Bitcoin's codebase is a commons: a shared resource that benefits everyone but no one owns. Traditional commons fail due to tragedy of the commons. Ostrom showed how to manage commons successfully. Bitcoin Commons applies these proven principles through cryptographic enforcement.

### How does this relate to cypherpunk philosophy?

Cypherpunks focused on eliminating trusted third parties in transactions. Bitcoin Commons extends this to development: reduce reliance on trusted parties in governance through cryptographic enforcement, transparency, and forkability. BLVM extends this to implementation: open specs, tests, review, and **BLVM Specification Lock** where applied—not a single blanket proof of every line.

## Technical Questions

### What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is a compiler-like infrastructure for Bitcoin implementations. It includes: (1) Orange Paper—complete mathematical specification serving as the IR (intermediate representation), (2) **blvm-consensus**—implementation **validated against** that spec (not generated from the IR), (3) optimization passes—runtime optimizations on the implementation, (4) **blvm-protocol**—Bitcoin abstraction layer, (5) **blvm-node**—full node implementation, (6) **blvm-sdk**—developer toolkit.

### What is the Orange Paper?

The Orange Paper is a complete mathematical specification of Bitcoin's consensus protocol, produced from analysis of the widely deployed implementation using AI-assisted extraction. It serves as the "intermediate representation" (IR) in BLVM's compiler-like architecture. The implementation is **validated against** this spec (not generated from it). **blvm-consensus** implements those rules with tests, review, and **BLVM Specification Lock** proofs on spec-locked code.

### How does formal verification work in BLVM?

BLVM uses **BLVM Specification Lock** (Z3) for formal proofs on spec-locked consensus functions, together with tests and review. The Orange Paper is the specification; **blvm-consensus** implements it. See [Formal Verification](../consensus/formal-verification.md).

### How is BLVM different from a typical full-node codebase?

Many deployments embed consensus in a large C++ codebase without a single companion IR like the Orange Paper. BLVM provides: (1) mathematical specification (Orange Paper), (2) **BLVM Specification Lock** (Z3 proofs on spec-locked code), (3) proofs co-located with code, (4) a compiler-like split (spec vs implementation) for alternative implementations. BLVM is a **different** development and verification stack, not a drop-in replacement for any one node.

### What does "compiler-like architecture" mean?

Like a compiler has a spec (IR) and implementation (machine code), BLVM has the Orange Paper as the spec (IR) and **blvm-consensus** as the implementation. The implementation is **validated against** the Orange Paper—it is not generated or transformed from the IR. Optimization passes optimize the implementation code. Multiple implementations can target the same Orange Paper; operating on mainnet also requires sound deployment and operations.

### What is formal verification in BLVM?

**BLVM Specification Lock** produces Z3 proofs for spec-locked functions against Orange Paper contracts. The Orange Paper remains the normative spec for the full rule set. See [Formal Verification](../consensus/formal-verification.md).

### How many formal proofs does BLVM have?

The set of spec-locked functions grows over time. Run `cargo spec-lock verify` in **blvm-consensus** or see [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md).

### What does "proofs locked to code" mean?

Spec-lock proofs live next to the functions they verify. Changing those functions requires updating proofs. Full proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

### How does BLVM prevent consensus bugs?

Through multiple layers: (1) Orange Paper specifies the rules, (2) Tests and integration catch regressions, (3) **BLVM Specification Lock** proves spec-locked consensus code against those rules, (4) Consensus logic lives in **blvm-consensus** so the node does not reimplement rules, (5) Review and tooling catch what automation misses. See [Formal Verification](../consensus/formal-verification.md).

### How does cryptographic enforcement work?

All governance actions require cryptographic signatures from maintainers. The governance-app (GitHub App) verifies signatures, enforces thresholds (e.g., 6-of-7), and blocks merges until requirements are met. This makes power visible and accountable: you can see who signed what, when.

### What BIPs are implemented?

BLVM implements numerous Bitcoin Improvement Proposals. See [Protocol Specifications](../reference/protocol-specifications.md) for a complete list, including consensus-critical BIPs (BIP65, BIP112, BIP68, BIP113, BIP125, BIP141/143, BIP340/341/342), network protocol BIPs (BIP152, BIP157/158, BIP331), and application-level BIPs (BIP21, BIP32/39/44, BIP174, BIP350/351).

### What storage backends are supported?

The node supports multiple storage backends. With `database_backend = "auto"` (default), the backend is chosen by build features: **RocksDB** when the `rocksdb` feature is enabled, then TidesDB, Redb, Sled. Options include **rocksdb** (can read common LevelDB-format chain state and `blk*.dat` layouts), **redb**, **sled**, and **tidesdb**. See [Storage Backends](../node/storage-backends.md) and [Configuration Reference](../reference/configuration-reference.md) for details.

### What transport protocols are supported?

The network layer supports multiple transport protocols: **TCP** (default, Bitcoin P2P compatible) and **Iroh/QUIC** (experimental). See [Network Protocol](../protocol/network-protocol.md) for details.

### How do I install BLVM?

Pre-built binaries are available from [GitHub Releases](https://github.com/BTCDecoded/blvm/releases). See [Installation](../getting-started/installation.md) for platform-specific instructions.

### What experimental features are available?

The experimental build variant includes: UTXO commitments, BIP119 CTV (CheckTemplateVerify), Dandelion++ privacy relay, BIP158, Stratum V2 mining protocol, and enhanced signature operations counting. See [Installation](../getting-started/installation.md#experimental-variant) for details.

### How do I configure the node?

Configuration can be done via config file (`blvm.toml`), environment variables, or command-line options. See [Node Configuration](../node/configuration.md) for complete configuration options.

### What RPC methods are available?

The node implements many JSON-RPC methods aligned with widely documented Bitcoin node RPC conventions across blockchain, raw transaction, mempool, network, mining, control, address, transaction, and payment categories. See [RPC API Reference](../node/rpc-api.md) for the list.

### How does the module system work?

The node includes a process-isolated module system that enables optional features (Lightning, merge mining, privacy enhancements) without affecting consensus or base node stability. Modules run in separate processes with IPC communication. See [Module Development](../sdk/module-development.md) for details.

### How do I troubleshoot issues?

See [Troubleshooting](../appendices/troubleshooting.md) for common issues and solutions, including node startup problems, storage issues, network connectivity, RPC configuration, module system issues, and performance optimization.
