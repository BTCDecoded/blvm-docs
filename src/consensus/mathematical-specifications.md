# Mathematical Specifications

**Canonical spec:** The [Orange Paper](../reference/orange-paper.md) on [thebitcoincommons.org](https://thebitcoincommons.org/orange-paper.html) ([Consensus Spec](https://thebitcoincommons.org/spec.html)). This page names the `blvm-consensus` functions for those formulas. Proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Functions

The formulas live in the Orange Paper. These are the Rust functions that implement them:

| Area | Functions |
|------|-----------|
| Chain selection | `should_reorganize`, `calculate_chain_work` |
| Subsidy and supply | `get_block_subsidy`, `total_supply` |
| Proof of work | `check_proof_of_work`, `expand_target`, `compress_target`, `get_next_work_required` |
| Transactions | `check_transaction`, `check_tx_inputs`, `is_coinbase`, `calculate_tx_id` |
| Block connection | `connect_block`, `apply_transaction` |
| Script | `eval_script`, `verify_script` |
| Peer commitment | `find_consensus`, `determine_checkpoint_height` |

How those checks are locked is [Formal verification](formal-verification.md) and [Assurance](assurance.md). Property tests are [Property-based testing](../development/property-based-testing.md).


## Source

Consensus-repo documents for this material ([docs/README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/README.md)):

- **[VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)** — how to run verification and what is in scope
- **[PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)** — proof bounds, coverage, and protections beyond formal verification

## See Also

- [Consensus Overview](overview.md) — Consensus layer introduction
- [Formal Verification](formal-verification.md) — BLVM Specification Lock methodology
- [Orange Paper](../reference/orange-paper.md) — Normative specification on Bitcoin Commons
- [Property-Based Testing](../development/property-based-testing.md) — Property-based testing
