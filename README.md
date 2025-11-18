# BLLVM Documentation

Unified documentation site for the Bitcoin Commons BLLVM ecosystem, built with [mdBook](https://rust-lang.github.io/mdBook/) and hosted on GitHub Pages.

## Overview

This repository aggregates documentation from all BLLVM source repositories into a single, navigable documentation site. Documentation is maintained in source repositories alongside code, and this repository serves as the orchestration layer that combines everything into a unified book.

**Live Site:** [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org)

## Structure

- `book.toml` - mdBook configuration
- `src/` - Documentation source files and navigation structure
- `modules/` - Git submodules pointing to source repositories
- `.github/workflows/` - Automated build and deployment

## Local Development

### Prerequisites

- [mdBook](https://rust-lang.github.io/mdBook/guide/installation.html) installed
- Git with submodule support

### Setup

1. Clone this repository with submodules:
   ```bash
   git clone --recursive https://github.com/BTCDecoded/bllvm-docs.git
   ```

2. If you already cloned without submodules:
   ```bash
   git submodule update --init --recursive
   ```

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

### Updating Submodules

To update submodules to their latest commits:

```bash
git submodule update --remote
```

## Documentation Sources

Documentation is aggregated from these source repositories:

- `modules/bllvm-spec/` - Orange Paper and specifications
- `modules/bllvm-consensus/` - Consensus layer documentation
- `modules/bllvm-protocol/` - Protocol layer documentation
- `modules/bllvm-node/` - Node implementation documentation
- `modules/bllvm-sdk/` - SDK documentation
- `modules/governance/` - Governance documentation
- `modules/bllvm/` - Build system and CLI documentation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to documentation.

## Deployment

Documentation is automatically built and deployed to GitHub Pages on every push to the `main` branch via GitHub Actions.

## License

MIT License - see [LICENSE](LICENSE) for details.

