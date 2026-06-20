# Contributing to BLVM Documentation

Thank you for your interest in improving BLVM documentation!

## Documentation philosophy

Most of the published book is authored in **`src/`** in this repository. A **small set** of pages embed upstream Markdown at build time using mdBook’s **`{{#include}}`** from a populated **`modules/`** directory (Orange Paper, governance narrative, and governance **config YAML** verified in CI—see `.github/workflows/deploy.yml`).

**Governance policy numbers** (tier/layer/emergency thresholds and review days) use **`[[gov:KEY]]`** placeholders expanded at build by **`mdbook-governance-vars`** from that YAML. Do not hand-edit those literals—change [governance](https://github.com/BTCDecoded/governance) `config/*.yml` and allowlisted keys in `mdbook-governance-vars/`. See [Contributing to Documentation](src/appendices/contributing-docs.md) for wired chapters and `docs/GOVERNANCE_MDBOOK.md` for the ADR.

Crate-specific guides (for example `blvm-consensus/docs/`) stay in those repositories; the unified site **links** to them or summarizes them here unless you add an explicit include.

**Where to contribute:**

- Cross-cutting book chapters and navigation → **`src/`** and **`src/SUMMARY.md`** in **blvm-docs**
- Deep component-only docs → the **source repository** for that crate (and link from this book if readers need the detail)

The full style guide and checklist live in the book as [Contributing to Documentation](src/appendices/contributing-docs.md) (*Appendices* in the built site). Prefer updating that file for standards so **CONTRIBUTING.md** (this file) stays a short entry point.

## Documentation standards

### Markdown format

- Use standard Markdown in upstream repos that are not mdBook-only; in **blvm-docs** `src/`, normal Markdown plus mdBook includes where wired.
- Follow consistent heading hierarchy.
- Use relative links for internal documentation.
- Include code examples where helpful.

### Style guidelines

- **Clarity**: Write clearly and concisely
- **Completeness**: Cover all important aspects
- **Examples**: Include practical examples
- **Links**: Link to related documentation
- **Code**: Include testable code examples where possible

### File organization

Each source repository may keep its own tree, for example:

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

## Contribution workflow

### For source repository documentation

1. Fork the source repository (e.g. `blvm-consensus`)
2. Make documentation improvements
3. Submit a pull request to that repository
4. After merge, the canonical text lives **there**; the public book picks it up when **blvm-docs** is updated (new or edited `src/` pages, refreshed links, or `{{#include}}` targets that point at your changes).

### For cross-cutting documentation

1. Fork this repository (`blvm-docs`)
2. Edit files under `src/` (not only submodules)
3. Submit a pull request
4. After merge, GitHub Actions rebuilds and deploys the site

### For navigation changes

1. Edit `src/SUMMARY.md` to add, remove, or reorder entries
2. Add or adjust content files as needed
3. Submit a pull request

## Local testing

1. Clone this repository:

   ```bash
   git clone https://github.com/BTCDecoded/blvm-docs.git
   ```

2. **Populate `modules/governance/`** — required when building chapters that `{{#include}}` governance prose or when running `./scripts/verify-book-inputs.sh`:

   - `modules/governance/README.md` and `modules/governance/GOVERNANCE.md`
   - (CI also requires `modules/governance/config/action-tiers.yml`, `repository-layers.yml`, and `emergency-tiers.yml` for deploy checks.)

   Clone from GitHub if needed ([governance](https://github.com/BTCDecoded/governance)). With a sibling checkout, from `blvm-docs/modules/`:

   ```bash
   ln -sf ../../governance governance
   ```

   The **[Orange Paper](https://thebitcoincommons.org/protocol.html)** is **not** included in this book—see [reference/orange-paper.md](src/reference/orange-paper.md).

3. Serve locally:

   ```bash
   mdbook serve
   ```

4. Open `http://localhost:3000` and review your changes.

5. Check links where appropriate:

   ```bash
   mdbook test
   ```

## Review process

- All documentation changes require review
- Maintainers will review for clarity, completeness, and accuracy
- Technical accuracy is especially important for consensus and protocol documentation

## Questions?

- Open an issue for questions about documentation structure
- Ask in GitHub Discussions for general questions
- Contact maintainers for repository-specific questions

Thank you for helping improve BLVM documentation!
