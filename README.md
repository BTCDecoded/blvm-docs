# BLVM Documentation

Unified documentation site for the Bitcoin Commons BLVM ecosystem, built with [mdBook](https://rust-lang.github.io/mdBook/) and hosted on GitHub Pages.

## Overview

This repository aggregates documentation from all BLVM source repositories into a single, navigable documentation site. Documentation is maintained in source repositories alongside code, and this repository serves as the orchestration layer that combines everything into a unified book.

**Live Site:** [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org)

## Structure

- `book.toml` - mdBook configuration
- `src/` - Documentation source files and navigation structure
- `modules/` - External sources included into the book (Orange Paper, governance); see Local Development
- `.github/workflows/` - Automated build and deployment

## Local Development

### Prerequisites

- [mdBook](https://rust-lang.github.io/mdBook/guide/installation.html) installed

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-docs.git
   ```

2. **Wire `modules/` includes** (required for `mdbook build`). Some pages use `{{#include}}` to embed:
   - `modules/blvm-spec/THE_ORANGE_PAPER.md`
   - `modules/governance/README.md` and `modules/governance/GOVERNANCE.md`

   Clone sources if needed: [blvm-spec](https://github.com/BTCDecoded/blvm-spec), [governance](https://github.com/BTCDecoded/governance). If you keep them as sibling directories next to `blvm-docs`, symlink from `blvm-docs/modules/`:
   ```bash
   cd blvm-docs/modules
   ln -sf ../../blvm-spec blvm-spec
   ln -sf ../../governance governance
   ```
   Adjust paths for your checkout. CI should populate `modules/` the same way before running `mdbook build`.

3. Serve the documentation locally:
   ```bash
   mdbook serve
   ```

   The documentation will be available at `http://localhost:3000`

4. Build the documentation:
   ```bash
   mdbook build
   ```

   Output will be in the `book/` directory.

### `modules/blvm` submodule

The optional **`modules/blvm`** git submodule is the **meta-repo** umbrella (`blvm`). Its `docs/` tree covers release/CI workflows for that repo. The **canonical** narrative for [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org) lives in **`src/`** in this repository.

## Documentation sources

- **`src/`** — primary book content and `SUMMARY.md` navigation.
- **`{{#include}}`** — pulls Orange Paper and governance files from **`modules/`** at build time (local files, not downloaded from GitHub during `mdbook build`).
- **Upstream crates** — consensus, protocol, node, SDK docs live in their repositories; this book links to them where needed.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [Contributing to BLVM Documentation](src/appendices/contributing-docs.md) (in the built book: *Appendices → Contributing to Documentation*).

## Deployment

Documentation is automatically built and deployed to GitHub Pages on every push to the `main` branch via GitHub Actions.

## License

MIT License - see [LICENSE](LICENSE) for details.
