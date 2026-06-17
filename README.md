# BLVM Documentation

Unified documentation site for the Bitcoin Commons BLVM ecosystem, built with [mdBook](https://rust-lang.github.io/mdBook/) and hosted on GitHub Pages.

## Overview

This repository builds the [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org) site with [mdBook](https://rust-lang.github.io/mdBook/). **Most chapters are written in `src/`** here. A **few** pages embed upstream Markdown at build time via mdBook's **`{{#include}}`**, which reads from a local **`modules/`** tree (Orange Paper, governance narrative, and governance **config YAML** checked in CI—see `.github/workflows/deploy.yml`). Governance policy numbers in wired chapters use **`[[gov:KEY]]`** placeholders expanded by **`mdbook-governance-vars`** at build time—edit [governance](https://github.com/BTCDecoded/governance) `config/*.yml`, not hand-copied literals (see `docs/GOVERNANCE_MDBOOK.md` and `mdbook-governance-vars/README.md`). Optional **git submodules** under `modules/` can mirror those repos for local work. Component-specific documentation (for example under `blvm-consensus/docs/`) remains in each crate's repository; this book **links** there or summarizes unless you add an explicit include.

**Live Site:** [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org)

## Structure

- `book.toml` - mdBook configuration
- `src/` - Documentation source files and navigation structure
- `modules/` - External sources included into the book (Orange Paper, governance); see Local Development
- `.github/workflows/` - Automated build and deployment

## Local Development

### Prerequisites

- [mdBook](https://rust-lang.github.io/mdBook/guide/installation.html) **0.4.43** (match `deploy.yml`)
- [Rust](https://rustup.rs/) (stable) for `mdbook-governance-vars`

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-docs.git
   ```

2. **Wire `modules/` includes** (required for `mdbook build`). Pages that use `{{#include}}` expect at least:
   - `modules/blvm-spec/THE_ORANGE_PAPER.md`
   - `modules/governance/README.md` and `modules/governance/GOVERNANCE.md`
   - Deploy CI also expects `modules/governance/config/action-tiers.yml`, `repository-layers.yml`, and `emergency-tiers.yml` (for policy parity checks); clone **governance** fully if you rely on those paths locally.

   Clone sources if needed: [blvm-spec](https://github.com/BTCDecoded/blvm-spec), [governance](https://github.com/BTCDecoded/governance). If you keep them as sibling directories next to `blvm-docs`, symlink from `blvm-docs/modules/`:
   ```bash
   cd blvm-docs/modules
   ln -sf ../../blvm-spec blvm-spec
   ln -sf ../../governance governance
   ```
   Adjust paths for your checkout. CI clones these repos instead of symlinks. If `git status` errors with *expected submodule path … not to be a symbolic link*, use `git -c submodule.recurse=false status` or `git submodule update --init` for `modules/governance` instead of a symlink.

3. **Install the governance preprocessor** (expands `[[gov:KEY]]` from YAML):
   ```bash
   cargo install --locked --path mdbook-governance-vars
   ```
   Optional checks (same order as CI):
   ```bash
   ./scripts/verify-book-inputs.sh   # includes governance literal check
   cargo test --locked --manifest-path mdbook-governance-vars/Cargo.toml
   ```
   The drift tests fail if `governance/config/*.yml` disagrees with `blvm-commons` `threshold.rs` (see `docs/GOVERNANCE_MDBOOK.md`).

4. Serve the documentation locally:
   ```bash
   mdbook serve
   ```

   The documentation will be available at `http://localhost:3000`

5. Build the documentation:
   ```bash
   mdbook build
   ```

   Output will be in the `book/` directory.

### `modules/blvm` submodule

The optional **`modules/blvm`** git submodule is the **meta-repo** umbrella (`blvm`). Its `docs/` tree covers release/CI workflows for that repo. The **canonical** narrative for [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org) lives in **`src/`** in this repository.

## Installation page

Install copy is generated from **`src/install/install-content.json`**. CI and local builds should refresh it from live **`blvm` GitHub Releases** before rendering:

```bash
node scripts/fetch-blvm-release.mjs && node scripts/render-installation.mjs
```

- **`deploy.yml`** and **`docs-pr.yml`** run fetch (`--strict`) then render before `mdbook build`.
- **`blvm` releases** dispatch `repository_dispatch(blvm-release)` to redeploy docs without a manual `blvm-docs` push.
- Static slot definitions: **`src/install/install-content.static.json`**; optional offline copy: **`install-content.fallback.json`**.

Do not edit **`getting-started/installation.md`** by hand. The [BTCDecoded website](https://github.com/BTCDecoded/website) uses its own **`fetch-blvm-release.mjs`** — do not run **`sync-install-data.mjs`** in CI.

## Documentation sources

- **`src/`** — primary narrative, `SUMMARY.md` navigation, and most chapters shipped on the site.
- **`{{#include}}`** — at `mdbook build`, pulls **specific** files from **`modules/`** (paths listed under Local Development). This is **not** a wholesale sync of every upstream doc; only wired paths are embedded.
- **Upstream repositories** — detailed per-crate docs and READMEs live beside code; the book links to GitHub or tells readers to run `cargo doc` where the [API Index](src/reference/api-index.md) describes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [Contributing to BLVM Documentation](src/appendices/contributing-docs.md) (in the built book: *Appendices → Contributing to Documentation*).

## Deployment

Documentation is automatically built and deployed to GitHub Pages on every push to the `main` branch via GitHub Actions.

## License

MIT License - see [LICENSE](LICENSE) for details.
