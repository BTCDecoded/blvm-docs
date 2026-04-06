# Contributing to BLVM Documentation

Thank you for your interest in improving BLVM documentation!

## Documentation Philosophy

Documentation is maintained in **source repositories** alongside code. This repository (`blvm-docs`) aggregates that documentation into a unified site. 

**Where to contribute:**
- Component-specific documentation → Edit in the source repository (e.g., `blvm-consensus/docs/`)
- Cross-cutting documentation → Edit in this repository (e.g., `blvm-docs/src/architecture/`)
- Navigation structure → Edit `SUMMARY.md` in this repository

## Documentation Standards

### Content principles (keep docs timeless and accurate)

- **Current state only** — Describe how things work and where things live now. Do not describe what was removed, refactored, or "we recently changed X."
- **No plan artifacts** — No task IDs, "Phase 2", "we removed X", or references to internal plans or WIP.
- **No unsubstantiated numbers** — Do not claim specific speedups (e.g. "10-50x faster") unless citing published benchmarks. Describe optimizations and point to benchmarks.thebitcoincommons.org or local runs.
- **Accurate feature status** — Do not label features as "deprecated" when they are actively reimplemented (e.g. BIP70).
- **IR vs implementation** — The Orange Paper is the spec (IR). The implementation is **validated against** it (e.g. blvm-spec-lock). Do not say the IR is "transformed" or "generated" into code.
- **API reference** — The canonical API reference is this book ([API Index](../reference/api-index.md), [SDK API Reference](../sdk/api-reference.md)). Do not point users to docs.rs as the primary API docs; link in-book or docs.thebitcoincommons.org.
- **Storage default** — `database_backend = "auto"` resolves by build features: RocksDB (if `rocksdb` feature) → TidesDB → Redb → Sled. Do not describe "redb" as the default without this context.
- **Paths** — Code links must use actual paths: `block/`, `script/` (dirs), `node/parallel_ibd/` (dir), blvm-protocol for spam_filter/utxo_commitments; no `block.rs`, `script.rs`, `parallel_ibd.rs` as single files, no utxostore_proofs.
- **Brittle links** — Prefer file or module links without line-number anchors (`#L123`). Line numbers break as code changes; use them only when pointing to a stable, narrow section and prefer "see `path/to/file.rs`" when the exact line is not critical.

When in doubt, see [DOC_UPDATE_PROPOSAL.md](https://github.com/BTCDecoded/blvm-docs/blob/main/DOC_UPDATE_PROPOSAL.md) (§1–3, §9–10) for editor context and checklist.

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
├── README.md                 # High-level overview
├── docs/
│   ├── README.md            # Documentation index
│   ├── architecture.md      # Component architecture
│   ├── guides/              # How-to guides
│   ├── reference/           # Reference documentation
│   └── examples/            # Code examples
```

## Contribution Workflow

### For Source Repository Documentation

1. Fork the source repository (e.g., `blvm-consensus`)
2. Make documentation improvements
3. Submit a pull request to the source repository
4. After merge, changes will appear in the unified documentation site (via `{{#include}}` directives)

### For Cross-Cutting Documentation

1. Fork this repository (`blvm-docs`)
2. Edit files in `src/` directory (not in submodules)
3. Submit a pull request
4. After merge, GitHub Actions will automatically rebuild and deploy

### For Navigation Changes

1. Edit `src/SUMMARY.md` to add/remove/modify navigation
2. Create corresponding content files if needed
3. Submit a pull request

## Local Testing

Before submitting changes:

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-docs.git
   ```

2. **Includes for Orange Paper and governance** — `mdbook build` fails if these paths are missing:
   - `modules/blvm-spec/THE_ORANGE_PAPER.md` (included from [Orange Paper](../reference/orange-paper.md))
   - `modules/governance/README.md` and `modules/governance/GOVERNANCE.md` (included from [Governance Overview](../governance/overview.md) and [Governance Model](../governance/governance-model.md))

   With sibling repo checkouts, from `blvm-docs/modules/`:
   ```bash
   ln -sf ../../blvm-spec blvm-spec
   ln -sf ../../governance governance
   ```
   Point the targets at your local `blvm-spec` and `governance` clones (paths may differ).

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
| **First-class modules** | Does each shipped module have a book page (not only a GitHub link)? |
| **Composition** | Is **`blvm-compose`** still accurately described if the composition API changed? |
| **Node config** | Do defaults (IBD, storage, pruning) match code and **configuration-reference**? |
| **Optional features** | If a feature is user-visible (e.g. WASM modules, extra transports), is it mentioned in the right node/sdk section? |

Add missing sections rather than assuming “the plan” covered developer ergonomics—those are easy to omit.

## Questions?

- Open an issue for questions about documentation structure
- Ask in GitHub Discussions for general questions
- Contact maintainers for repository-specific questions

Thank you for helping improve BLVM documentation!
