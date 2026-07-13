# Contributing to BLVM Documentation

## Documentation Philosophy

The public book is built from **`blvm-docs`**: most content is authored in **`src/`**. A **small, explicit** set of pages uses mdBook **`{{#include}}`** to embed files from a local **`modules/`** checkout (governance narrative and governance **config YAML** verified in deploy CI). The Orange Paper and Consensus Spec live on [thebitcoincommons.org](https://thebitcoincommons.org), see [Orange Paper](../reference/orange-paper.md). Crate-specific documentation (e.g. `blvm-consensus/docs/`) stays in those repositories; this book **links** to them or summarizes them unless you add another include.

**Where to contribute:**
- Component-specific documentation → Edit in the source repository (e.g., `blvm-consensus/docs/`)
- Cross-cutting documentation → Edit in this repository (e.g., `blvm-docs/src/architecture/`)
- Navigation structure → Edit [book navigation](https://github.com/BTCDecoded/blvm-docs/blob/main/src/SUMMARY.md) in this repository

## Documentation Standards

### Content principles (keep docs timeless and accurate)

- **Diátaxis type**: Optional HTML comment on page 1: `<!-- diataxis: tutorial | how-to | reference | explanation -->` (see [Operator guide](../getting-started/operator-guide.md), [Developer guide](../getting-started/developer-guide.md) for hub examples).

- **Current state only**: Describe how things work and where things live now. Do not describe what was removed, refactored, or "we recently changed X."
- **No plan artifacts**: No task IDs, "Phase 2", "we removed X", or references to internal plans or WIP.
- **No unsubstantiated numbers**: Do not claim specific speedups (e.g. "10-50x faster") unless citing published benchmarks. Describe optimizations and point to benchmarks.thebitcoincommons.org or local runs.
- **Governance policy numbers**: Tier, layer, emergency, and matrix thresholds use **`[[gov:KEY]]`** placeholders (expanded at build from [governance](https://github.com/BTCDecoded/governance) `config/*.yml`). Wired chapters include PR process, contributing, layer-tier model, multisig configuration, keyholder procedures, governance fork/model, component relationships, module system, SDK overview/getting-started/examples/api-reference, quick-start, security controls, FAQ/glossary, and related captions. CI runs `scripts/check-governance-literals.sh` on those files. **Do not hand-edit** `N-of-M` literals; change YAML upstream and add allowlisted keys in `mdbook-governance-vars` if needed. Tier 5 special process remains prose + links to [governance policy](https://github.com/BTCDecoded/governance/blob/main/GOVERNANCE.md) / [action tiers](https://github.com/BTCDecoded/governance/blob/main/docs/ACTION_TIERS.md).
- **Accurate feature status**: Do not label features as "deprecated" when they are actively reimplemented (e.g. BIP70).
- **IR vs implementation**: The Orange Paper is the spec (IR). The implementation is **validated against** it (e.g. blvm-spec-lock). Do not say the IR is "transformed" or "generated" into code.
- **API reference**: The canonical API reference is this book ([API Index](../reference/api-index.md), [SDK API Reference](../sdk/api-reference.md)). Do not point users to docs.rs as the primary API docs; link in-book or docs.thebitcoincommons.org.
- **Storage default**: `database_backend = "auto"` resolves by build features: heed3 (if `heed3` feature) → RocksDB → TidesDB → Redb → Sled. Do not describe "redb" or "RocksDB" as the default without this context.
- **Paths**: Code links must use actual paths: `block/`, `script/` (dirs), `node/parallel_ibd/` (dir), blvm-protocol for spam_filter/utxo_commitments; no `block.rs`, `script.rs`, `parallel_ibd.rs` as single files, no utxostore_proofs.
- **Brittle links**: Prefer file or module links without line-number anchors (`#L123`). Line numbers break as code changes; use them only when pointing to a stable, narrow section and prefer "see `path/to/file.rs`" when the exact line is not critical.
- **No meta openers**: Do not restate the page title ("This document explains…", "This guide covers…"). Start with substance.
- **No hedge labels**: Avoid `(illustrative)`, `(non-binding)`, "napkin math", and similar disclaimers. Either cite a benchmark source, give a concrete example with its assumptions, or say figures depend on deployment, once, without stacking qualifiers.
- **Plain adjectives**: Cut filler (`comprehensive`, `robust`, `seamless`, `unified`) when they add no information. Prefer what the code actually does.
- **Experimental compile-time features**: Flag sections that need non-`production` builds with a blockquote at the section or page top: `> **Experimental build**: …` linking to [Installation: experimental variant](../getting-started/installation.md#experimental-variant).
- **Admonitions**: Use HTML callouts for operator-critical notes (styles in `custom.css`):

```html
<div class="admonition danger">
<div class="admonition-title">Danger</div>
Stop bitcoind before migrating a Core datadir.
</div>
```

Types: `note`, `tip`, `warning`, `danger`. Prefer these over bare bold for data-loss or security-critical instructions.

Follow the **Content principles** above and the [Contributing](../development/contributing.md) chapter.

### Markdown Format

- Use standard Markdown (no mdBook-specific syntax in source repos)
- Follow consistent heading hierarchy
- Use relative links for internal documentation
- Include code examples where helpful

### Style Guidelines

- **Clarity**: Write clearly and concisely
- **Completeness**: Cover all important aspects
- **Examples**: Include practical examples
- **Links**: Link to related documentation
- **Code**: Include testable code examples where possible

### File Organization

Each source repository should maintain documentation in:

```
repository-root/
├── README.md # High-level overview
├── docs/
│ ├── README.md # Documentation index
│ ├── architecture.md # Component architecture
│ ├── guides/ # How-to guides
│ ├── reference/ # Reference documentation
│ └── examples/ # Code examples
```

## Contribution Workflow

### For Source Repository Documentation

1. Fork the source repository (e.g., `blvm-consensus`)
2. Make documentation improvements
3. Submit a pull request to the source repository
4. After merge, the canonical prose lives in **that** repository; it appears on the documentation site when **blvm-docs** is updated (new or edited `src/` chapters, refreshed links, or `{{#include}}` sources that point at your changes).

### For Cross-Cutting Documentation

1. Fork this repository (`blvm-docs`)
2. Edit files in `src/` directory (not in submodules)
3. Submit a pull request
4. After merge, GitHub Actions will automatically rebuild and deploy

### For Navigation Changes

1. Edit [book navigation](https://github.com/BTCDecoded/blvm-docs/blob/main/src/SUMMARY.md) to add/remove/modify navigation
2. Create corresponding content files if needed
3. Submit a pull request

## Local Testing

Before submitting changes:

1. Clone the repository:
 ```bash
 git clone https://github.com/BTCDecoded/blvm-docs.git
 ```

2. **Governance includes**: `mdbook build` needs these paths when governance chapters use `{{#include}}`:

 - [governance README](https://github.com/BTCDecoded/governance/blob/main/README.md) and [governance policy](https://github.com/BTCDecoded/governance/blob/main/GOVERNANCE.md) (included from [Governance Overview](../governance/overview.md) and [Governance Model](../governance/governance-model.md))
 - Deploy CI also requires `modules/governance/config/action-tiers.yml`, `repository-layers.yml`, and `emergency-tiers.yml` (policy data alongside prose).

 Clone [governance](https://github.com/BTCDecoded/governance) if needed. With a sibling checkout, from `blvm-docs/modules/`:
 ```bash
 ln -sf ../../governance governance
 ```

 The **[Orange Paper](https://thebitcoincommons.org/orange-paper.html)** and **[Consensus Spec](https://thebitcoincommons.org/spec.html)** are on the Bitcoin Commons website, not embedded here. This book links via [Orange Paper](../reference/orange-paper.md).

3. Serve locally:
 ```bash
 mdbook serve
 ```

4. Review changes at `http://localhost:3000`

5. Check for broken links:
 ```bash
 mdbook test
 ```

### `modules/blvm` submodule

The **`modules/blvm`** submodule is the **meta-repo** (`blvm` build/orchestration tree). Its `docs/` tree is for umbrella workflows and release tooling, **not** the same as this book’s `src/`. Prefer editing cross-cutting narrative in **`blvm-docs/src/`** unless the change belongs to meta-repo CI or release docs only.

## Review Process

- All documentation changes require review
- Maintainers will review for clarity, completeness, and accuracy
- Technical accuracy is especially important for consensus and protocol documentation

## Major documentation update checklist

When refreshing docs for a release or large refactor, explicitly verify (not only path fixes):

| Area | Ask |
|------|-----|
| **SDK / modules** | Are `blvm-sdk` **module** APIs documented? (`#[module]`, `run_module!`, prelude, `blvm-sdk-macros`) |
| **User CLI** | Do modules that register CLI document **`blvm <group> …`** and that the module must be loaded? |
| **New crates** | Is every user-facing crate listed in stack overview, glossary, and **api-index**? |
| **First-class modules** | Does each shipped module have a book page (not only a GitHub link)? Modules may be **omitted from `SUMMARY.md`** deliberately (source kept under `src/modules/` but not built into the public book). |
| **Composition** | Is **`blvm-compose`** still accurately described if the composition API changed? |
| **Node config** | Do defaults (IBD, storage, pruning) match code and **configuration-reference**? |
| **Optional features** | If a feature is user-visible (e.g. WASM modules, extra transports), is it mentioned in the right node/sdk section? |

Add missing sections rather than assuming “the plan” covered developer ergonomics, those are easy to omit.

## Questions?

- Open an issue for questions about documentation structure
- Ask in GitHub Discussions for general questions
- Contact maintainers for repository-specific questions
