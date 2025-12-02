# Glossary

Key terms and concepts used throughout the BLVM documentation.

## BLVM Components

**BLVM** (Bitcoin Low-Level Virtual Machine) - Compiler-like infrastructure for Bitcoin implementations. Transforms the [Orange Paper](orange-paper.md) (IR) through [optimization passes](../consensus/architecture.md#optimization-passes) into optimized code, with [formal verification](../consensus/formal-verification.md) ensuring correctness. Similar to how LLVM provides compiler infrastructure, BLVM provides Bitcoin implementation infrastructure.

**Orange Paper** - Mathematical specification of Bitcoin's consensus protocol, serving as the "intermediate representation" (IR) in BLVM's compiler-like architecture. Transformed through [optimization passes](../consensus/architecture.md#optimization-passes) into optimized code. See [Orange Paper](orange-paper.md).

**Optimization Passes** - Runtime optimization passes in [bllvm-consensus](../consensus/overview.md) that transform the [Orange Paper](orange-paper.md) specification into optimized code: Pass 2 (Constant Folding), Pass 3 (Memory Layout Optimization), Pass 5 (SIMD Vectorization), plus bounds check optimization, dead code elimination, and inlining hints. See [Optimization Passes](../consensus/architecture.md#optimization-passes).

**bllvm-consensus** - Optimized mathematical implementation of Bitcoin consensus rules with [formal verification](../consensus/formal-verification.md) ([Kani proofs](../consensus/formal-verification.md)). Includes [optimization passes](../consensus/architecture.md#optimization-passes) that transform the [Orange Paper](orange-paper.md) specification into production-ready code. Foundation layer with no dependencies. See [Consensus Overview](../consensus/overview.md).

**bllvm-protocol** - Protocol abstraction layer for multiple Bitcoin variants (mainnet, testnet, regtest) while maintaining consensus compatibility. See [Protocol Overview](../protocol/overview.md).

**bllvm-node** - Bitcoin node implementation with [storage](../node/storage-backends.md), [networking](../node/transport-abstraction.md), [RPC](../node/rpc-api.md), and [mining](../node/mining.md) capabilities. Production-ready reference implementation. See [Node Overview](../node/overview.md).

**bllvm-sdk** - Developer toolkit providing [governance cryptographic primitives](../governance/overview.md), [module composition framework](../architecture/module-system.md), and CLI tools for key management and signing. See [SDK Overview](../sdk/overview.md).

## Governance

**Bitcoin Commons** - Forkable governance framework applying Elinor Ostrom's commons management principles through cryptographic enforcement. See [Governance Overview](../governance/overview.md).

**5-Tier Governance Model** - Constitutional governance system with graduated signature thresholds (3-of-5 to 6-of-7) and review periods (7 days to 365 days) based on change impact. See [Layer-Tier Model](../governance/layer-tier-model.md).

**Forkable Governance** - Governance rules can be forked by users if they disagree with decisions, creating exit competition and preventing capture. See [Governance Fork](../governance/governance-fork.md).

**Cryptographic Enforcement** - All governance actions require cryptographic signatures from maintainers, making power visible and accountable. See [Keyholder Procedures](../governance/keyholder-procedures.md).

**Economic Node Veto** - Tier 3 consensus-adjacent changes can be vetoed by [economic nodes](../governance/economic-nodes.md) representing 30%+ hashpower or 40%+ economic activity.

## Technical Concepts

**Formal Verification** - Mathematical proof of code correctness using [Kani model checking](../consensus/formal-verification.md). BLVM has [201 formal proofs](../consensus/formal-verification.md) embedded in the codebase.

**Proofs Locked to Code** - [Formal verification](../consensus/formal-verification.md) proofs are embedded in the code itself, ensuring correctness is maintained as code changes.

**Spec Drift Detection** - Automated detection when implementation code diverges from the [Orange Paper](orange-paper.md) mathematical specification.

**Compiler-Like Architecture** - Architecture where [Orange Paper](orange-paper.md) (IR) → [optimization passes](../consensus/architecture.md#optimization-passes) → [bllvm-consensus](../consensus/overview.md) → [bllvm-node](../node/overview.md), similar to source code → IR → optimization passes → machine code in compilers. See [System Overview](../architecture/system-overview.md).

**Process Isolation** - [Module system](../architecture/module-system.md) design where each module runs in a separate process with isolated memory, preventing failures from propagating to the base node.

**IPC** (Inter-Process Communication) - Communication mechanism between modules and the node using Unix domain sockets with length-delimited binary messages. See [Module IPC Protocol](../architecture/module-ipc-protocol.md).

## Storage & Networking

**Storage Backends** - Database backends for blockchain data: **redb** (default, production-ready), **sled** (beta, fallback), **auto** (auto-select based on availability). See [Storage Backends](../node/storage-backends.md).

**Pruning** - Storage optimization that removes old block data while keeping the UTXO set. Configurable to keep last N blocks.

**Transport Abstraction** - Unified abstraction supporting multiple transport protocols: **TCP** (default, Bitcoin P2P compatible) and **Iroh/QUIC** (experimental). See [Transport Abstraction](../node/transport-abstraction.md).

**Network Variants** - Bitcoin network types: **Mainnet** (BitcoinV1, production), **Testnet3** (test network), **Regtest** (regression testing, isolated).

## Consensus & Protocol

**Consensus Rules** - Mathematical rules that all Bitcoin nodes must follow to maintain network consensus. Defined in the [Orange Paper](orange-paper.md) and implemented in [bllvm-consensus](../consensus/overview.md).

**BIP** (Bitcoin Improvement Proposal) - Standards for Bitcoin protocol changes. BLVM implements numerous BIPs including BIP30, BIP34, BIP66, BIP90, BIP147, BIP141/143, BIP340/341/342. See [Protocol Specifications](protocol-specifications.md).

**SegWit** (Segregated Witness) - [BIP141/143](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) implementation separating witness data from transaction data, enabling transaction malleability fixes and capacity improvements.

**Taproot** - [BIP340/341/342](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) implementation providing Schnorr signatures, Merkle tree scripts, and improved privacy.

**RBF** (Replace-By-Fee) - BIP125 implementation allowing transaction replacement with higher fees before confirmation.

## Development

**Module System** - [Process-isolated system](../architecture/module-system.md) supporting optional features ([Lightning](../modules/lightning.md), [merge mining](../node/mining-stratum-v2.md), privacy enhancements) without affecting consensus or base node stability.

**Module Manifest** (`module.toml`) - Configuration file defining module metadata, capabilities, dependencies, and entry point.

**Capabilities** - Permissions system for modules: `read_blockchain`, `read_utxo`, `read_chain_state`, `subscribe_events`, `send_transactions` (future).

**RPC** (Remote Procedure Call) - [JSON-RPC 2.0 interface](../node/rpc-api.md) for interacting with the node. BLVM implements Bitcoin Core-compatible methods.

## Governance Phases

**Phase 1** (Infrastructure Building) - All core components are implemented. Governance is not activated. Test keys are used.

**Phase 2** (Governance Activation) - Governance rules are enforced with real cryptographic keys and keyholder onboarding.

**Phase 3** (Full Operation) - Mature, stable system with battle-tested governance and production deployment.
