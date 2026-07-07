# Design Philosophy

BLVM is built for teams who need Bitcoin consensus correctness to be **checkable**, protocol evolution to be **bounded**, and node features to be **extensible without touching consensus**. The principles below are the reasoning behind that shape—not slogans.

## Core Principles

### 1. Mathematical correctness first

**Problem:** Hand-wavy “Bitcoin-compatible” implementations drift from mainnet rules under edge cases (witness nesting, sighash variants, soft-fork activation boundaries).

**Alternative:** Interpret Bitcoin Core’s C++ informally and patch when differential tests fail.

**Choice:** The [Orange Paper](../reference/orange-paper.md) is the normative spec—written so consensus can be reviewed in mathematical notation without reading implementation code. **blvm-consensus** implements it; **BLVM Specification Lock**, differential testing, fuzzing, and review keep the code aligned with that document. Pure functions where the design allows so behavior is reproducible in tests and proofs.

### 2. Layered architecture

**Problem:** Monolithic nodes mix networking bugs with consensus bugs; upgrades become risky all-or-nothing releases.

**Alternative:** Microservices with shared mutable state (harder to reason about than a disciplined monolith).

**Choice:** Strict crate layers: spec → consensus → protocol → node → SDK → governance tooling. Lower layers do not depend on RPC or modules. Each layer can be tested and versioned independently within release sets.

### 3. Zero consensus re-implementation

**Problem:** A payment module or RPC handler that “fixes” validation logic creates a fork risk invisible until mainnet.

**Alternative:** Allow application code to call internal consensus helpers with ad hoc flags.

**Choice:** All rule changes flow through **blvm-consensus**. **blvm-protocol** varies network parameters and message framing; **blvm-node** orchestrates I/O. Modules run out-of-process and cannot rewrite the UTXO set or block acceptance rules.

### 4. Cryptographic governance

**Problem:** Open-source governance often relies on social consensus alone; capture and silent policy drift are hard to detect.

**Alternative:** Fully automated on-chain governance (inappropriate for a node implementation project).

**Choice:** Apply Bitcoin-style multisig and audit trails to **repository and release policy** ([governance](../governance/overview.md)). Power is visible; changing security-critical code requires documented tiers and signatures—not a single maintainer click.

### 5. User sovereignty

**Problem:** Forced upgrades and opaque defaults push operators onto configurations they did not choose.

**Alternative:** Infinite per-user consensus forks in one binary (unmaintainable).

**Choice:** Operators pick network, features, and modules. Governance is forkable: disagree with policy → run a fork with transparent rules rather than hidden behavior in a shared binary.

## Design Decisions (expanded)

### Why pure functions in consensus?

Deterministic, side-effect-free validation makes **differential testing against Core**, property tests, and spec-lock proofs tractable. The cost is explicit data passing (UTXO views, flags) instead of hidden global state—which is appropriate for consensus.

### Why formal verification alongside tests?

Tests cannot exhaust script and block combinatorics. **BLVM Specification Lock** (Z3) regression-tests spec-derived contracts on annotated functions; differential testing compares BLVM against Bitcoin Core on mainnet history; fuzzing and proptest explore generated inputs. Neither layer replaces the others—all are in the merge gate where applicable. Spec-lock is **consensus conformance**, not side-channel resistance (that lives in **blvm-secp256k1** for secret-path crypto). The Orange Paper remains the human-auditable spec. See [Formal Verification — scope](../consensus/formal-verification.md#scope-and-limits).

### Why process-isolated modules?

In-process plugins are faster but share address space with the node. **Choice:** optional features (Lightning, Stratum, ZMQ, mesh) as separate processes with capability-based IPC. A module crash should not corrupt chainstate; a malicious module should not get write access to consensus state.

### Why cryptographic governance instead of policy docs only?

Policy PDFs do not enforce themselves on GitHub. Wiring security-control classification into PR tiers makes “who must sign this change?” a machine-checkable question for contributors. Operators still rely on [Deployment posture](../security/deployment-posture.md) for runtime exposure—not this system.

## Trade-offs

| Tension | Choice | Mitigation |
|---------|--------|------------|
| Performance vs correctness | Correctness first | Profile after correctness gates; PGO and batch validation in hot paths |
| Flexibility vs safety | Safety first | Protocol abstraction for experiments without consensus edits |
| Simplicity vs features | Simplicity in consensus | Features in node/modules; consensus grows only via spec + BIP process |

## Design Evolution

BLVM targets long-horizon Bitcoin infrastructure:

- **Protocol evolution** through **blvm-protocol** variants and BIPs, not ad hoc node patches
- **Feature addition** via modules and optional compile-time features (experimental builds)
- **Governance evolution** through documented tier changes, not silent CI edits
- **Multiple implementations** sharing the Orange Paper as common IR

## See Also

- [Stack overview](system-overview.md) — Six-layer stack summary
- [Crate dependencies](component-relationships.md) — Dependency graph
- [Consensus Overview](../consensus/overview.md) — How correctness is structured in code
- [Governance Overview](../governance/overview.md) — Cryptographic governance
- [Orange Paper](../reference/orange-paper.md) — Mathematical foundation
