# Consensus Layer Overview

**blvm-consensus** answers one question: given a transaction, block, UTXO set, and activation flags, does Bitcoin consensus accept it? It does not open sockets, read `blvm.toml`, or choose mainnet vs regtest—that belongs to [blvm-protocol](../protocol/overview.md) and [blvm-node](../node/overview.md).

## What this layer is for

Consensus code is the **trust anchor** of the stack. Wallets, pools, and modules depend on the node reporting chain state that matches what every other Bitcoin mainnet participant would accept. If validation is wrong here, every higher layer is wrong.

The layer implements rules from the [Orange Paper](../reference/orange-paper.md) as deterministic Rust: script execution, block connection, subsidy and difficulty math, mempool acceptance rules used by the node, and soft-fork behavior at documented activation heights.

## Relationship to the Orange Paper

The Orange Paper is the **specification** (treated as an intermediate representation). **blvm-consensus** is the **implementation**, checked by:

- Unit, integration, and [differential tests](../development/differential-testing.md) (full-chain harness in **blvm-bench**)
- [Formal verification](formal-verification.md) via **BLVM Specification Lock** on spec-locked functions
- Review and CI gates on security-critical paths

The implementation is **not generated** from the Orange Paper; it is **validated against** it. Optimization passes (constant folding, batch script verification) speed the code without changing the specified meaning.

**Chain of trust:**

```
Orange Paper → blvm-consensus → tests + spec-lock → node deployment
```

Details: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md), [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## What lives here vs elsewhere

| Concern | Layer |
|---------|--------|
| Script/block/UTXO math | **blvm-consensus** (this page) |
| Network magic, ports, message serialization | [blvm-protocol](../protocol/overview.md) |
| Storage, P2P, RPC, modules | [blvm-node](../node/overview.md) |
| Fast sync (UTXO commitments, peer consensus, spam filtering) | [node docs](../node/utxo-commitments.md) (**blvm-protocol** / **blvm-node**, not consensus rules) |
| Orange Paper function catalog & Rust API names | [API Index — Consensus](../reference/api-index.md#consensus-layer-blvm-consensus) |

## Architecture position

**Stack layer 2** — between the Orange Paper (layer 1) and protocol abstraction (layer 3). Full stack: [Introduction](../introduction.md#what-is-blvm).

## Design principles

1. **Pure functions** — Deterministic validation; explicit inputs instead of hidden globals
2. **No rule interpretation in apps** — Node calls into consensus; modules never patch rules
3. **Controlled dependencies** — `Cargo.toml` pins and ranges are the source of truth for crypto and BLVM crates
4. **Testing in depth** — [Testing](../development/testing.md), [property-based tests](../development/property-based-testing.md), [differential testing](../development/differential-testing.md) via **blvm-bench**
5. **Formal verification** — Spec-lock proofs complement tests; see [Formal Verification](formal-verification.md)

## Formal verification (summary)

Critical properties (chain work, subsidy halving, proof of work, transaction structure, `connect_block` UTXO consistency) are among the primary verification targets. CI runs spec-lock on annotated functions; coverage and limitations are documented in the consensus repo.

## BIP implementation

Consensus integrates consensus-critical BIPs in validation paths—for example BIP30/34/66/90/147 in block connection and script verification. Activation heights and network variants are coordinated with **blvm-protocol** network parameters.

## Performance

Consensus hot paths support PGO builds (`./scripts/pgo-build.sh` in **blvm-consensus**), batch script verification, and documented optimization passes. Optimize after correctness gates; measure on your workload.

## Dependencies

Declare versions from [`blvm-consensus` `Cargo.toml`](https://github.com/BTCDecoded/blvm-consensus/blob/main/Cargo.toml). **blvm-primitives** supplies shared types; consensus re-exports many for API stability.

## Source code

| Area | Repository path |
|------|-----------------|
| Crate root | [blvm-consensus](https://github.com/BTCDecoded/blvm-consensus) |
| Transactions / scripts | `src/transaction.rs`, `src/script/` |
| Blocks / chain | `src/block/` |
| Economic rules | `src/economic.rs` |
| Mempool rules | `src/mempool.rs` |
| Mining helpers | `src/mining.rs` |
| SegWit / Taproot | `src/segwit.rs` |
| Optimizations | `src/optimizations.rs` |

## See Also

- [API Index — Consensus functions](../reference/api-index.md#consensus-function-catalog-orange-paper-names)
- [Consensus Architecture](architecture.md) — Internal design
- [Formal Verification](formal-verification.md) — Methodology
- [Orange Paper](../reference/orange-paper.md) — Normative spec
