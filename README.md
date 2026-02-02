# BLVM Documentation

Unified documentation site for the Bitcoin Commons BLVM ecosystem, built with [mdBook](https://rust-lang.github.io/mdBook/) and hosted on GitHub Pages.

## Overview

This repository aggregates documentation from all BLVM source repositories into a single, navigable documentation site. Documentation is maintained in source repositories alongside code, and this repository serves as the orchestration layer that combines everything into a unified book.

**Live Site:** [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org)

## Structure

- `book.toml` - mdBook configuration
- `src/` - Documentation source files and navigation structure
- `.github/workflows/` - Automated build and deployment

## Local Development

### Prerequisites

- [mdBook](https://rust-lang.github.io/mdBook/guide/installation.html) installed

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-docs.git
   ```

2. Serve the documentation locally:
   ```bash
   mdbook serve
   ```

   The documentation will be available at `http://localhost:3000`

3. Build the documentation:
   ```bash
   mdbook build
   ```

   Output will be in the `book/` directory.

## Documentation Sources

Documentation is aggregated from source repositories using `{{#include}}` directives that fetch content from GitHub. Documentation is maintained in source repositories alongside code.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to documentation.

## Deployment

Documentation is automatically built and deployed to GitHub Pages on every push to the `main` branch via GitHub Actions.

## License

MIT License - see [LICENSE](LICENSE) for details.

