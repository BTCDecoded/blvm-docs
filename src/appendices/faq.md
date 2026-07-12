# Frequently Asked Questions

Short answers for operators and developers. **Project positioning** (Bitcoin Commons narrative, governance framing): [thebitcoincommons.org FAQ](https://thebitcoincommons.org/#faq).

Governance philosophy and tier mechanics: [Governance Overview](../governance/overview.md) and [Governance Model](../governance/governance-model.md).

## General

### What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is compiler-like infrastructure for Bitcoin: the [Orange Paper](../reference/orange-paper.md) spec, **blvm-consensus**, **blvm-protocol**, **blvm-node**, and **blvm-sdk**. See [Introduction](../introduction.md).

### Is this a fork of Bitcoin?

No. BLVM does not fork Bitcoin’s chain or consensus rules. It implements the same consensus rules as mainnet Bitcoin.

### Is the system production ready?

BLVM publishes a full node stack, crates, tests, and formal verification tooling, but **readiness depends on your deployment** and project phase: apply your own security review, RPC hardening, and monitoring. Governance enforcement is **not universally activated** (Phase 1; test keys). See [Deployment posture](../security/deployment-posture.md) and [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md). “Artifacts exist” is accurate; “production mainnet node with live governance” is not yet.

### Where is the code?

Repositories under [BTCDecoded](https://github.com/BTCDecoded) (e.g. `blvm`, `blvm-node`, `blvm-consensus`). The umbrella release binary is built from the `blvm` crate.

## Running a node

### How do I install BLVM?

Pre-built packages and binaries: **[btcdecoded.org/install](https://btcdecoded.org/install)** (current release). Platform/feature notes: [Installation](../getting-started/installation.md). Verify checksums on every download.

### How do I run my first node?

[Quick Start](../getting-started/quick-start.md) (regtest, ~5 minutes) or [First Node Setup](../getting-started/first-node.md) (config file; [mainnet IBD](../getting-started/first-node.md#mainnet-initial-sync) for first sync).

### What must I do before mainnet?

See [Deployment posture](../security/deployment-posture.md): RPC auth, bind addresses, release verification, backups, and module supply chain.

### How do I configure the node?

`blvm.toml`, CLI flags, and `BLVM_*` environment variables. Precedence: CLI > ENV > file > defaults. [Node Configuration](../node/configuration.md), [Configuration Reference](../reference/configuration-reference.md).

### Can I start from an existing Bitcoin Core datadir?

Yes, with the **`rocksdb`** feature (**`blvm` default features**; portable Windows/aarch64 release builds use redb/sled instead): stop **`bitcoind`**, point **`--data-dir`** at a synced Core tree, migrate once to **`<datadir>/blvm/`**. See [Operations: Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir).

### What storage backends are supported?

`database_backend = "auto"` (usually **heed3** in default builds), or explicit **rocksdb**, **redb**, **sled**, **tidesdb**. See [Storage Backends](../node/storage-backends.md).

### What experimental compile-time features exist?

Stable GitHub Releases ship **platform-specific** feature sets (see [Release process: Build variants](../development/release-process.md#build-variants)). **`blvm` default features** (local `cargo build` and Linux x86_64 release artifacts) include Dandelion++, Iroh, UTXO commitments, BIP70/REST, and **`compression`**; portable **Windows** and **Linux aarch64** release CI builds omit several of those. BIP119 CTV, Stratum V2 node demux, sigop counting, and Quinn still often need explicit `--features`. See [Installation: experimental variant](../getting-started/installation.md#experimental-variant).

### What RPC methods are available?

JSON-RPC aligned with common Bitcoin node docs, plus BLVM-specific and module-extended methods. See [RPC API Reference](../node/rpc-api.md) and the parity table there.

### How do I troubleshoot?

[Appendix: Troubleshooting](troubleshooting.md). Mainnet IBD: [Troubleshooting: Mainnet IBD](troubleshooting.md#mainnet-ibd).

## Governance

Questions operators and new contributors often ask before reading the full governance docs.

### Do I need governance to run a node?

No. Running a BLVM node does not require tiers, multisig, or governance tooling. Use the [Operator guide](../getting-started/operator-guide.md) and [Deployment posture](../security/deployment-posture.md). Governance applies when you contribute code, review PRs, or sign releases.

### What is Bitcoin Commons vs BLVM?

BLVM is the technical stack (spec, node, SDK). Bitcoin Commons is the governance framework (tiers, signatures, fork rules). They are related but serve different roles. See [Governance Overview](../governance/overview.md).

### What are layers, tiers, and signatures?

**Layers** map repo areas (consensus, protocol, node, modules). **Tiers** set how many signatures a change needs. **Signatures** are cryptographic approvals from registered keyholders. Constitutional layers need more signatures than extension layers. Details: [Governance Model](../governance/governance-model.md), [Layer-Tier Model](../governance/layer-tier-model.md).

### Why “6x harder to capture”?

Bitcoin Commons applies graduated signature thresholds and review periods so capturing governance requires compromising many independent keyholders across layers, not a single maintainer group. See [Governance Model](../governance/governance-model.md).

## Modules and development

### How does the module system work?

Optional features run in isolated processes with IPC. See [Module catalog](../modules/overview.md) and [Building modules](../sdk/module-development.md).

### Can I build my own module?

Yes. Start with [Building your first module](../getting-started/first-module.md), then [Building modules](../sdk/module-development.md).

### How can I contribute?

[Contributing](../development/contributing.md), [Contributing to Documentation](contributing-docs.md).

### What documentation should I read?

Use the [Introduction: Who is this for](../introduction.md#who-is-this-for) paths. Operators: Getting Started + Node + Security. Developers: SDK + Modules. Researchers: Orange Paper + Formal Verification.

## Spec and verification

### What is the Orange Paper?

The normative mathematical specification of Bitcoin consensus, the reference “IR” for BLVM. **[protocol specification](https://thebitcoincommons.org/protocol.html)** states consensus rules in implementation-agnostic mathematical notation so reviewers (including mathematicians who do not read Rust or C++) can audit rules directly. Hosted on [thebitcoincommons.org](https://thebitcoincommons.org/orange-paper.html) with the auditable [Consensus Spec](https://thebitcoincommons.org/spec.html) as the primary rule register. This book: [Orange Paper](../reference/orange-paper.md).

### What is the primary verification artifact?

**The Orange Paper** is the normative spec. **BLVM Specification Lock** (Z3), differential testing, fuzzing, and proptest are downstream enforcement; they keep the Rust implementation aligned with that spec; they do not replace it. See [Formal Verification](../consensus/formal-verification.md).

### Is formal verification “proof instead of testing”?

**No.** Philosophy: **Rust + Tests + Math Specs = Source of Truth**. Spec-lock regression-tests spec-derived contracts on annotated consensus functions; differential testing compares BLVM against Bitcoin Core across mainnet history; fuzz and proptest cover generated inputs. All layers are in the merge gate where applicable. [Formal Verification](../consensus/formal-verification.md), [Differential Testing](../development/differential-testing.md).

### Does spec-lock prove constant-time cryptography?

**No.** Spec-lock checks **consensus conformance** (functional properties from the Orange Paper). **Side-channel resistance** for secret-path crypto is handled in **`blvm-secp256k1`** (signing, pubkey-from-secret, ECDH); consensus **verification** uses variable-time math on public inputs only, the same correct split as libsecp256k1. See [Formal Verification](../consensus/formal-verification.md#what-formal-verification-delivers) and [blvm-secp256k1 timing policy](https://github.com/BTCDecoded/blvm-secp256k1/blob/main/TIMING.md).

### How does formal verification work?

**BLVM Specification Lock** links `#[spec_locked]` Rust functions to Orange Paper contracts; Z3 checks those obligations on merge. Inventory and policy: [spec-lock coverage inventory](https://github.com/BTCDecoded/blvm-spec-lock/blob/main/SPEC_LOCK_COVERAGE.md), [verification policy](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md). Full stack: [Formal Verification](../consensus/formal-verification.md).
