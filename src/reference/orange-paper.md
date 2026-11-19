# Orange Paper

The normative Bitcoin consensus specification lives on **[thebitcoincommons.org](https://thebitcoincommons.org)**. This manual, at **[docs.btcdecoded.org/blvm](https://docs.btcdecoded.org/blvm/)**, documents how BLVM implements and operates on the network. The commons site hosts the auditable spec text itself.

## Where to read the spec

Bitcoin Commons publishes several linked viewers, all sourced from [blvm-spec](https://github.com/BTCDecoded/blvm-spec) on GitHub:

| Page | Source file | Open it when |
|------|-------------|--------------|
| [**Consensus Spec**](https://thebitcoincommons.org/spec.html) | `CONSENSUS_SPEC.md` | You need a numbered consensus requirement (MUST / SHOULD / MAY), tied to an Orange Paper §ref and `blvm-consensus`. Primary entry. |
| [**Orange Paper**](https://thebitcoincommons.org/orange-paper.html) | `THE_ORANGE_PAPER.md` | You want the full formal model and how the documents relate. Navigation hub for PROTOCOL, ARCHITECTURE, and related definitions. |
| [**PROTOCOL**](https://thebitcoincommons.org/protocol.html) | `PROTOCOL.md` | You want the math for a rule: functions, invariants, proofs, preconditions, and postconditions. |
| [**ARCHITECTURE**](https://thebitcoincommons.org/architecture.html) | `ARCHITECTURE.md` | You want how the spec maps onto implementation structure and how the pieces compose. |

To run a node, configure RPC, or deploy modules, stay in this book: [Introduction](../introduction.md), [First node](../getting-started/first-node.md).

Cross-links between viewers rewrite internal markdown references (for example `§5.3.1` in the Consensus Spec jumps to the matching section in PROTOCOL or ARCHITECTURE). The [homepage spec section](https://thebitcoincommons.org/#path-orange-paper) includes an interactive structure map (sunburst) over Orange Paper content. The [spec visualizations](https://thebitcoincommons.org/spec-viz/index.html) page on the commons site has the interactive views of Orange Paper sections.

The **Orange Paper** name refers to the extended formal specification (`THE_ORANGE_PAPER.md` and its PROTOCOL / ARCHITECTURE companions). In BLVM discussions it is also treated as the **intermediate representation (IR)**—the reference against which **blvm-consensus** is validated, not generated.

## Source and changes

All spec markdown is maintained in **[blvm-spec](https://github.com/BTCDecoded/blvm-spec)** (Layer 1 constitutional repo). The commons viewers fetch live content from GitHub; edit the markdown there and open a pull request—do not expect the full spec text in **blvm-docs**.

## In BLVM

[blvm-consensus](../consensus/overview.md) implements these rules. [BLVM Specification Lock](../consensus/formal-verification.md), tests, and review validate code against the spec. The Orange Paper is the IR—the implementation is **not** generated from it. See [compiler-like architecture](glossary.md#compiler-like-architecture).

## See also

- [Stack overview](../architecture/system-overview.md)
- [Bitcoin Commons homepage](https://thebitcoincommons.org)
