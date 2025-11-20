# Glossary

Key terms and concepts used throughout the BLLVM documentation.

## BLLVM Components

**BLLVM** (Bitcoin Low-Level Virtual Machine) - The technical stack providing mathematical rigor for Bitcoin implementations through the Orange Paper, formal verification, and compiler-like architecture.

**Orange Paper** - Complete mathematical specification of Bitcoin's consensus protocol, serving as the "intermediate representation" (IR) in BLLVM's compiler-like architecture.

**bllvm-consensus** - Pure mathematical implementation of Bitcoin consensus rules with formal verification (Kani proofs). Foundation layer with no dependencies.

**bllvm-protocol** - Protocol abstraction layer enabling support for multiple Bitcoin variants (mainnet, testnet, regtest) while maintaining consensus compatibility.

**bllvm-node** - Full Bitcoin node implementation with storage, networking, RPC, and mining capabilities. Production-ready reference implementation.

**bllvm-sdk** - Developer toolkit providing governance cryptographic primitives, module composition framework, and CLI tools for key management and signing.

## Governance

**Bitcoin Commons** - Forkable governance framework applying Elinor Ostrom's commons management principles through cryptographic enforcement. Provides coordination without civil war.

**5-Tier Governance Model** - Constitutional governance system with graduated signature thresholds (3-of-5 to 6-of-7) and review periods (7 days to 365 days) based on change impact.

**Forkable Governance** - Governance rules can be forked by users if they disagree with decisions, creating exit competition and preventing capture.

**Cryptographic Enforcement** - All governance actions require cryptographic signatures from maintainers, making power visible and accountable.

**Economic Node Veto** - Tier 3 consensus-adjacent changes can be vetoed by economic nodes representing 30%+ hashpower or 40%+ economic activity.

## Technical Concepts

**Formal Verification** - Mathematical proof of code correctness using Kani model checking. BLLVM has nearly 200 formal proofs embedded in the codebase.

**Proofs Locked to Code** - Formal verification proofs are embedded in the code itself, ensuring correctness is maintained as code changes.

**Spec Drift Detection** - Automated detection when implementation code diverges from the Orange Paper mathematical specification.

**Compiler-Like Architecture** - Architecture where Bitcoin Core code → Orange Paper (IR) → bllvm-consensus → bllvm-node, similar to source code → IR → machine code in compilers.

**Process Isolation** - Module system design where each module runs in a separate process with isolated memory, preventing failures from propagating to the base node.

**IPC** (Inter-Process Communication) - Communication mechanism between modules and the node using Unix domain sockets with length-delimited binary messages.

## Storage & Networking

**Storage Backends** - Database backends for blockchain data: **redb** (default, production-ready), **sled** (beta, fallback), **auto** (auto-select based on availability).

**Pruning** - Storage optimization that removes old block data while keeping the UTXO set. Configurable to keep last N blocks.

**Transport Abstraction** - Unified abstraction supporting multiple transport protocols: **TCP** (default, Bitcoin P2P compatible) and **Iroh/QUIC** (experimental).

**Network Variants** - Bitcoin network types: **Mainnet** (BitcoinV1, production), **Testnet3** (test network), **Regtest** (regression testing, isolated).

## Consensus & Protocol

**Consensus Rules** - Mathematical rules that all Bitcoin nodes must follow to maintain network consensus. Defined in the Orange Paper and implemented in bllvm-consensus.

**BIP** (Bitcoin Improvement Proposal) - Standards for Bitcoin protocol changes. BLLVM implements numerous BIPs including BIP65, BIP112, BIP125, BIP141/143, BIP340/341/342.

**SegWit** (Segregated Witness) - BIP141/143 implementation separating witness data from transaction data, enabling transaction malleability fixes and capacity improvements.

**Taproot** - BIP340/341/342 implementation providing Schnorr signatures, Merkle tree scripts, and improved privacy.

**RBF** (Replace-By-Fee) - BIP125 implementation allowing transaction replacement with higher fees before confirmation.

## Development

**Module System** - Process-isolated system enabling optional features (Lightning, merge mining, privacy enhancements) without affecting consensus or base node stability.

**Module Manifest** (`module.toml`) - Configuration file defining module metadata, capabilities, dependencies, and entry point.

**Capabilities** - Permissions system for modules: `read_blockchain`, `read_utxo`, `read_chain_state`, `subscribe_events`, `send_transactions` (future).

**RPC** (Remote Procedure Call) - JSON-RPC 2.0 interface for interacting with the node. BLLVM implements 28 Bitcoin Core-compatible methods.

## Status & Phases

**Phase 1** (Infrastructure Building) - Current phase where all core components are implemented but governance is not yet activated. Test keys only.

**Phase 2** (Governance Activation) - Future phase when governance rules will be enforced with real cryptographic keys and keyholder onboarding.

**Phase 3** (Full Operation) - Future phase representing mature, stable system with battle-tested governance and production deployment.
