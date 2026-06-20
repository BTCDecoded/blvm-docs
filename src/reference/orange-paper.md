# Orange Paper

The normative Bitcoin consensus specification lives on **[thebitcoincommons.org](https://thebitcoincommons.org)**—not inside this book. **docs.thebitcoincommons.org** (this site) documents how BLVM implements and operates on the network; the commons site hosts the auditable spec text itself.

**Read the Orange Paper:** [thebitcoincommons.org/orange-paper.html](https://thebitcoincommons.org/orange-paper.html) · **Consensus Spec (rule register):** [spec.html](https://thebitcoincommons.org/spec.html)

## Where to read the spec

Bitcoin Commons publishes several linked viewers, all sourced from [blvm-spec](https://github.com/BTCDecoded/blvm-spec) on GitHub:

| Page | Source file | Role |
|------|-------------|------|
| [**Consensus Spec**](https://thebitcoincommons.org/spec.html) | `CONSENSUS_SPEC.md` | **Primary entry** — numbered rules in RFC 2119 language, each tied to Orange Paper §refs and `blvm-consensus` |
| [**Orange Paper**](https://thebitcoincommons.org/orange-paper.html) | `THE_ORANGE_PAPER.md` | Extended formal spec — navigation hub for PROTOCOL, ARCHITECTURE, and related definitions |
| [**PROTOCOL**](https://thebitcoincommons.org/protocol.html) | `PROTOCOL.md` | Formal consensus mathematics (functions, invariants, proofs) |
| [**ARCHITECTURE**](https://thebitcoincommons.org/architecture.html) | `ARCHITECTURE.md` | Implementation design and how spec pieces compose |

Cross-links between viewers rewrite internal markdown references (for example `§5.3.1` in the Consensus Spec jumps to the matching section in PROTOCOL or ARCHITECTURE). The [homepage spec section](https://thebitcoincommons.org/#path-orange-paper) includes an interactive structure map (sunburst) over Orange Paper content.

## Which page should I open?

| Goal | Start here |
|------|------------|
| Audit a specific consensus requirement (MUST / SHOULD / MAY) | [Consensus Spec](https://thebitcoincommons.org/spec.html) |
| Understand the full formal model and how documents relate | [Orange Paper](https://thebitcoincommons.org/orange-paper.html) |
| Read detailed math for a rule (functions, pre/postconditions) | [PROTOCOL](https://thebitcoincommons.org/protocol.html) |
| See how spec maps to implementation structure | [ARCHITECTURE](https://thebitcoincommons.org/architecture.html) |
| Run a node, configure RPC, modules, deployment | This book — [Introduction](../introduction.md), [First node](../getting-started/first-node.md) |

The **Orange Paper** name refers to the extended formal specification (`THE_ORANGE_PAPER.md` and its PROTOCOL / ARCHITECTURE companions). In BLVM discussions it is also treated as the **intermediate representation (IR)**—the reference against which **blvm-consensus** is validated, not generated.

## Source and changes

All spec markdown is maintained in **[blvm-spec](https://github.com/BTCDecoded/blvm-spec)** (Layer 1 constitutional repo). The commons viewers fetch live content from GitHub; edit the markdown there and open a pull request—do not expect the full spec text in **blvm-docs**.

## In BLVM

[blvm-consensus](../consensus/overview.md) implements these rules. [BLVM Specification Lock](../consensus/formal-verification.md), tests, and review validate code against the spec. The Orange Paper is the IR—the implementation is **not** generated from it. See [compiler-like architecture](glossary.md#compiler-like-architecture).

## See also

- [Consensus overview](../consensus/overview.md)
- [Consensus architecture](../consensus/architecture.md)
- [Formal verification](../consensus/formal-verification.md)
- [Stack overview](../architecture/system-overview.md)
- [Bitcoin Commons homepage](https://thebitcoincommons.org)
