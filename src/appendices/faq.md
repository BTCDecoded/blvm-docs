# Frequently Asked Questions

## General Questions

### What is Bitcoin Commons?

Bitcoin Commons is a project that solves Bitcoin's governance asymmetry through two complementary innovations: [BLVM](../introduction.md) (the technical stack providing mathematical rigor) and Bitcoin Commons (the governance framework providing coordination without civil war). Together, they enable safe alternative Bitcoin implementations with forkable governance. See [Introduction](../introduction.md) and [Governance Overview](../governance/overview.md) for details.

### How is this different from Bitcoin Core?

Bitcoin Core is a single implementation with informal governance. Bitcoin Commons provides: (1) BLVM - Mathematical rigor enabling safe alternatives, (2) Commons - Forkable governance enabling coordination. Bitcoin Core has excellent consensus security; Bitcoin Commons adds governance security and implementation diversity.

### Is this a fork of Bitcoin?

No. Neither BLVM nor Bitcoin Commons forks Bitcoin's blockchain or consensus rules. BLVM provides mathematical specification enabling safe alternative implementations. Bitcoin Commons provides governance framework enabling coordination. Both maintain full Bitcoin consensus compatibility.

### Is the system production ready?

BLVM provides a complete Bitcoin node implementation with all core components. The system includes formal verification, comprehensive testing, and production-ready features. For production deployment, ensure proper security hardening, RPC authentication, and monitoring are configured. See [Node Configuration](../node/configuration.md) and [Security](../security/security-controls.md) for production considerations.

### How do BLVM and Bitcoin Commons work together?

BLVM provides the mathematical foundation and compiler-like architecture (Orange Paper as IR, formal verification passes). Bitcoin Commons provides the governance framework (coordination without civil war). The modular architecture is where both meet: BLVM ensures correctness through architectural enforcement; Commons ensures coordination through governance rules. You can't have safe alternative implementations without BLVM's mathematical rigor, and you can't have coordination without Commons' governance framework.

### What are the two innovations?

**BLVM (Bitcoin Low-Level Virtual Machine)**: Technical innovation providing mathematical rigor through the [Orange Paper](../reference/orange-paper.md) (mathematical specification), [formal verification](../consensus/formal-verification.md) ([Z3 proofs via BLVM Specification Lock](../consensus/formal-verification.md)), proofs locked to code, and a compiler-like architecture. This ensures correctness. See [Introduction](../introduction.md) and [Consensus Overview](../consensus/overview.md) for details.

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

BLVM solves the technical problem (mathematical rigor, safe alternative implementations). Bitcoin Commons solves the governance problem (coordination without civil war). You can't have safe alternatives without BLVM's mathematical foundation, and you can't have coordination without Commons' governance framework. They enable each other.

### How does the modular architecture combine both innovations?

The modular architecture has three layers: (1) Mandatory Consensus (BLVM ensures correctness), (2) Optional Modules (Commons enables competition), (3) Economic Coordination (module marketplace funds infrastructure). BLVM ensures correctness through architectural enforcement; Commons ensures coordination through governance rules. The architecture is where both meet.

### Can you use BLVM without Bitcoin Commons governance?

Technically yes: BLVM is a technical stack that can be used independently. However, without Bitcoin Commons governance, you'd still have the governance capture problem. The innovations are designed to work together: BLVM enables safe alternatives, Commons enables coordination between alternatives.

### Can you use Bitcoin Commons governance without BLVM?

The governance framework could theoretically be applied to other implementations, but BLVM's mathematical rigor (Orange Paper, formal verification) is what makes alternative implementations safe. Without BLVM, you'd have governance but still risk consensus bugs from informal implementations.

### What happens if governance is captured?

Forkable governance means users can fork to a better governance model. This creates exit competition: captured governance loses users to better-governed implementations. The threat of forking prevents capture. Unlike Bitcoin Core, you can fork the governance rules, not just the code.

### How does economic alignment work?

Through the module marketplace. Module authors receive 75% of sales, Commons receives 15% for infrastructure, and node operators receive 10%. This creates sustainable funding while incentivizing quality module development.

### What is merge mining?

Merge mining is available as a separate paid plugin module (`blvm-merge-mining`). It allows miners to mine multiple blockchains simultaneously using the same proof-of-work. However, merge mining is not a Commons funding model - revenue goes to the module developer, not to Commons infrastructure.

### What features does BLVM provide?

Orange Paper complete, blvm-consensus with formal proofs, blvm-protocol, blvm-node, and blvm-sdk all implemented. All 6 tiers are functional and production-ready.

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

Cypherpunks focused on eliminating trusted third parties in transactions. Bitcoin Commons extends this to development: eliminate trusted parties in governance through cryptographic enforcement, transparency, and forkability. BLVM extends this to implementation: eliminate trusted implementations through mathematical proof.

## Technical Questions

### What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is a compiler-like infrastructure for Bitcoin implementations, similar to how LLVM provides compiler infrastructure for programming languages. It includes: (1) Orange Paper - complete mathematical specification serving as the IR (intermediate representation), (2) Optimization Passes - runtime optimization passes (constant folding, memory layout optimization, SIMD vectorization, bounds check optimization, dead code elimination), (3) blvm-consensus - optimized mathematical implementation with formal verification, (4) blvm-protocol - Bitcoin abstraction layer, (5) blvm-node - full node implementation, (6) blvm-sdk - developer toolkit. The optimization passes transform the Orange Paper specification into optimized, production-ready code.

### What is the Orange Paper?

The Orange Paper is a complete mathematical specification of Bitcoin's consensus protocol, extracted from Bitcoin Core using AI-assisted analysis. It serves as the "intermediate representation" (IR) in BLVM's compiler-like architecture. It enables safe alternative implementations by providing formal, verifiable consensus rules that can be mathematically proven correct.

### How does formal verification work in BLVM?

BLVM uses BLVM Specification Lock (with Z3) to formally verify consensus-critical code. The Orange Paper provides the mathematical specification; blvm-consensus implements it with proofs locked to code. All consensus decisions flow through verified functions, and the dependency chain prevents bypassing verification. This provides mathematical proof of correctness, not just testing.

### How is BLVM different from Bitcoin Core?

Bitcoin Core embeds consensus rules in 350,000+ lines of C++ with no mathematical specification. BLVM provides: (1) Mathematical specification (Orange Paper), (2) Formal verification (Z3 proofs via BLVM Specification Lock), (3) Proofs locked to code, (4) Compiler-like architecture enabling safe alternative implementations. BLVM doesn't replace Bitcoin Core; it enables safe alternatives.

### What does "compiler-like architecture" mean?

Like a compiler has source code → IR → optimization passes → machine code, BLVM has: Bitcoin Core code → Orange Paper (IR) → optimization passes → blvm-consensus → blvm-node. The Orange Paper serves as the intermediate representation that gets transformed through optimization passes (constant folding, memory layout optimization, SIMD vectorization, bounds check optimization, dead code elimination) into optimized code. Just like multiple compilers can target the same LLVM IR, multiple Bitcoin implementations can target the Orange Paper specification. This enables implementation diversity while maintaining consensus correctness through shared mathematical foundations.

### What is formal verification in BLVM?

BLVM uses BLVM Specification Lock (with Z3) to mathematically prove code correctness. The Orange Paper provides the specification; blvm-consensus implements it with proofs. All consensus decisions flow through verified functions. This provides mathematical proof, not just testing.

### How many formal proofs does BLVM have?

BLVM has comprehensive formal proofs in the source code, providing formal verification coverage of consensus-critical functions. The proofs are embedded directly in the codebase and verified continuously.

### What does "proofs locked to code" mean?

Formal verification proofs are embedded in the code itself, not separate documentation. The proofs verify that the code matches the Orange Paper specification. If code changes, proofs must be updated, ensuring correctness is maintained.

### How does BLVM prevent consensus bugs?

Through multiple layers: (1) Orange Paper provides mathematical specification, (2) Formal verification proves implementation matches spec, (3) Proofs locked to code prevent drift, (4) Dependency chain forces all consensus through verified functions, (5) Spec drift detection alerts if code diverges from spec.

### How does cryptographic enforcement work?

All governance actions require cryptographic signatures from maintainers. The governance-app (GitHub App) verifies signatures, enforces thresholds (e.g., 6-of-7), and blocks merges until requirements are met. This makes power visible and accountable: you can see who signed what, when.

### What BIPs are implemented?

BLVM implements numerous Bitcoin Improvement Proposals. See [Protocol Specifications](../reference/protocol-specifications.md) for a complete list, including consensus-critical BIPs (BIP65, BIP112, BIP68, BIP113, BIP125, BIP141/143, BIP340/341/342), network protocol BIPs (BIP152, BIP157/158, BIP331), and application-level BIPs (BIP21, BIP32/39/44, BIP174, BIP350/351).

### What storage backends are supported?

The node supports multiple storage backends with automatic fallback: **redb** (default, recommended), **sled** (beta, fallback option), and **auto** (auto-select based on availability). See [Node Configuration](../node/configuration.md) for details.

### What transport protocols are supported?

The network layer supports multiple transport protocols: **TCP** (default, Bitcoin P2P compatible) and **Iroh/QUIC** (experimental). See [Network Protocol](../protocol/network-protocol.md) for details.

### How do I install BLVM?

Pre-built binaries are available from [GitHub Releases](https://github.com/BTCDecoded/blvm/releases). See [Installation](../getting-started/installation.md) for platform-specific instructions.

### What experimental features are available?

The experimental build variant includes: UTXO commitments, BIP119 CTV (CheckTemplateVerify), Dandelion++ privacy relay, BIP158, Stratum V2 mining protocol, and enhanced signature operations counting. See [Installation](../getting-started/installation.md#experimental-variant) for details.

### How do I configure the node?

Configuration can be done via config file (`blvm.toml`), environment variables, or command-line options. See [Node Configuration](../node/configuration.md) for complete configuration options.

### What RPC methods are available?

The node implements 28 Bitcoin Core-compatible JSON-RPC methods across blockchain, raw transaction, mempool, network, and mining categories. See [RPC API Reference](../node/rpc-api.md) for the complete list.

### How does the module system work?

The node includes a process-isolated module system that enables optional features (Lightning, merge mining, privacy enhancements) without affecting consensus or base node stability. Modules run in separate processes with IPC communication. See [Module Development](../sdk/module-development.md) for details.

### How do I troubleshoot issues?

See [Troubleshooting](../appendices/troubleshooting.md) for common issues and solutions, including node startup problems, storage issues, network connectivity, RPC configuration, module system issues, and performance optimization.
