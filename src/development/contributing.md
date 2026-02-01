# Contributing to BLVM

Thank you for your interest in contributing to BLVM (Bitcoin Low-Level Virtual Machine)! This guide covers the complete developer workflow from setting up your environment to getting your changes merged.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](https://github.com/BTCDecoded/.github/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- **Rust 1.70 or later** - Check with `rustc --version`
- **Git** - For version control
- **Cargo** - Included with Rust
- **Text editor or IDE** - Your choice

### Development Setup

1. **Fork the repository** you want to contribute to (e.g., [blvm-consensus](https://github.com/BTCDecoded/blvm-consensus), [blvm-protocol](https://github.com/BTCDecoded/blvm-protocol), [blvm-node](https://github.com/BTCDecoded/blvm-node))
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blvm-consensus.git
   cd blvm-consensus
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/BTCDecoded/blvm-consensus.git
   ```
4. **Build the project**:
   ```bash
   cargo build
   ```
5. **Run tests**:
   ```bash
   cargo test
   ```

## Contribution Workflow

### 1. Create a Feature Branch

Always create a new branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

**Branch naming conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Your Changes

Follow these guidelines when making changes:

#### Code Style

- **Follow Rust conventions** - Use `cargo fmt` to format code
- **Run clippy** - Use `cargo clippy -- -D warnings` to check for improvements
- **Write clear, self-documenting code** - Code should be readable without excessive comments

#### Testing

- **Write tests for all new functionality** - See [Testing Infrastructure](testing.md) for details
- **Ensure existing tests continue to pass** - Run `cargo test` before committing
- **Add integration tests** for complex features
- **Aim for high test coverage** - Consensus-critical code requires >95% coverage

#### Documentation

- **Document all public APIs** - Use Rust doc comments (`///`)
- **Update README files** when adding features
- **Include code examples** in documentation
- **Follow Rust documentation conventions**

### 3. Commit Your Changes

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Commit types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `test` - Test additions/changes
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `ci` - CI/CD changes
- `chore` - Maintenance tasks

**Examples**:
```
feat(consensus): add OP_CHECKSIGVERIFY implementation
fix(node): resolve connection timeout issue
docs(readme): update installation instructions
test(block): add edge case tests for block validation
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub. See the [PR Process](pr-process.md) for details on governance tiers, review periods, and maintainer signatures. Your PR should include:
- **Clear title** - Describes what the PR does
- **Detailed description** - Explains the changes and why
- **Reference issues** - Link to related issues if applicable
- **Checklist** - Mark items as you complete them (see PR Checklist below)

## Repository-Specific Guidelines

### blvm-consensus

**Critical**: This code implements Bitcoin consensus rules. Any changes must:

- **Match Bitcoin Core behavior exactly** - No deviations
- **Not deviate from the [Orange Paper](../reference/orange-paper.md) specifications** - Mathematical correctness required
- **Handle all edge cases correctly** - Consensus code must be bulletproof
- **Maintain mathematical precision** - No approximations

**Additional requirements**:
- **Exact Version Pinning**: All consensus-critical dependencies must be pinned to exact versions
- **Pure Functions**: All functions must remain side-effect-free
- **Testing**: All mathematical functions must be thoroughly tested (see [Testing Infrastructure](testing.md))
- **Formal Verification**: Consensus-critical changes may require blvm_spec_lock proofs

### blvm-protocol

- **Protocol Abstraction**: Changes must maintain clean abstraction
- **Variant Support**: Ensure all Bitcoin variants continue to work
- **Backward Compatibility**: Avoid breaking changes to protocol interfaces

### blvm-node

- **Consensus Integrity**: Never modify consensus rules (use blvm-consensus for that)
- **Production Readiness**: Consider production deployment implications
- **Performance**: Maintain reasonable performance characteristics

## Pull Request Checklist

Before submitting your PR, ensure:

- [ ] **All tests pass** - Run `cargo test` locally
- [ ] **Code is formatted** - Run `cargo fmt`
- [ ] **No clippy warnings** - Run `cargo clippy -- -D warnings`
- [ ] **Documentation is updated** - Public APIs documented, README updated if needed
- [ ] **Commit messages follow conventions** - Use conventional commit format
- [ ] **Changes are focused and atomic** - One logical change per PR
- [ ] **Repository-specific guidelines followed** - See section above

## Review Process

### What Happens After You Submit a PR

1. **Automated CI runs** - Tests, linting, and checks run automatically
2. **Governance tier classification** - Your PR is automatically classified into a [governance tier](../governance/layer-tier-model.md)
3. **Maintainers review** - Code review by project maintainers
4. **Signatures required** - Maintainers must cryptographically sign approval (see [PR Process](pr-process.md))
5. **Review period** - Tier-specific review period must elapse (see [PR Process](pr-process.md) for details)
6. **Merge** - Once all requirements are met, your PR is merged

### Review Criteria

Reviewers will check:

- **Correctness** - Does the code work as intended?
- **Consensus compliance** - Does it match Bitcoin Core? (for consensus code)
- **Test coverage** - Are all cases covered?
- **Performance** - No regressions?
- **Documentation** - Is it clear and complete?
- **Security** - Any potential vulnerabilities?

### Getting Your PR Reviewed

- **Be patient** - Review periods vary by tier (7-180 days)
- **Respond to feedback** - Address review comments promptly
- **Keep PRs small** - Smaller PRs are reviewed faster
- **Update PR description** - Keep it current as you make changes

## Governance Tiers

Your PR will be automatically classified into a governance tier based on the changes. See [PR Process](pr-process.md) for detailed information about:

- **Tier 1: Routine Maintenance** - Bug fixes, documentation, performance optimizations (7 day review, see [Layer-Tier Model](../governance/layer-tier-model.md))
- **Tier 2: Feature Changes** - New RPC methods, P2P changes, wallet features (30 day review)
- **Tier 3: Consensus-Adjacent** - Changes affecting consensus validation code (90 day review)
- **Tier 4: Emergency Actions** - Critical security patches (0 day review)
- **Tier 5: Governance Changes** - Changes to governance rules (180 day review)

## Testing Your Changes

See [Testing Infrastructure](testing.md) for testing documentation. Key points:

- **Unit tests** - Test individual functions
- **Integration tests** - Test cross-module functionality
- **[Property-based testing](property-based-testing.md)** - Test with generated inputs
- **[Fuzzing](fuzzing.md)** - Find edge cases automatically
- **[Differential testing](differential-testing.md)** - Compare with Bitcoin Core behavior

## CI/CD Workflows

When you push code or open a PR, automated workflows run:

- **Tests** - All test suites run
- **Linting** - Code style and quality checks
- **Coverage** - Test coverage analysis
- **Build verification** - Ensures code compiles

See [CI/CD Workflows](ci-cd-workflows.md) for detailed information about what runs and how to debug failures.

## Getting Help

- **Discussions** - Use GitHub Discussions for questions
- **Issues** - Use GitHub Issues for bugs and feature requests
- **Security** - Use private channels for security issues (see SECURITY.md in each repo)

## Recognition

Contributors will be recognized in:

- Repository CONTRIBUTORS.md files
- Release notes for significant contributions
- Organization acknowledgments

## Questions?

If you have questions about contributing:

1. Check existing discussions and issues
2. Open a new discussion
3. Contact maintainers privately for sensitive matters

Thank you for contributing to BLVM!

## See Also

- [PR Process](pr-process.md) - Pull request review process and governance tiers
- [CI/CD Workflows](ci-cd-workflows.md) - What happens when you push code
- [Testing Infrastructure](testing.md) - Testing guides
- [Release Process](release-process.md) - How releases are created

