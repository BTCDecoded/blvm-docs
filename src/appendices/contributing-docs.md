# Contributing to BLVM Documentation

Thank you for your interest in improving BLVM documentation!

## Documentation Philosophy

Documentation is maintained in **source repositories** alongside code. This repository (`blvm-docs`) aggregates that documentation into a unified site. 

**Where to contribute:**
- Component-specific documentation → Edit in the source repository (e.g., `blvm-consensus/docs/`)
- Cross-cutting documentation → Edit in this repository (e.g., `blvm-docs/src/architecture/`)
- Navigation structure → Edit `SUMMARY.md` in this repository

## Documentation Standards

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

2. Serve locally:
   ```bash
   mdbook serve
   ```

3. Review changes at `http://localhost:3000`

4. Check for broken links:
   ```bash
   mdbook test
   ```

## Review Process

- All documentation changes require review
- Maintainers will review for clarity, completeness, and accuracy
- Technical accuracy is especially important for consensus and protocol documentation

## Questions?

- Open an issue for questions about documentation structure
- Ask in GitHub Discussions for general questions
- Contact maintainers for repository-specific questions

Thank you for helping improve BLVM documentation!
