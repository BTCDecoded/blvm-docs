# Contributing to BLVM

Developer workflow from environment setup through merge.

New to the project? Read [Repository layout](repository-architecture.md) first — why Bitcoin Commons uses separate repositories, how the crates fit together, and how local development and CI differ.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](https://github.com/BTCDecoded/.github/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- **Rust toolchain**: Each repository sets a minimum in **`Cargo.toml`** (`rust-version`, **edition 2024** on current workspace crates). Use **`rustc --version`** and satisfy the **`rust-version`** of the **crate you are building**. For a workspace that pulls multiple crates, the effective floor is the **maximum** `rust-version` among packages you compile — see **[MSRV note](msrv-note.md)** (currently **1.85**; CI pins **1.88**).
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
- **Aim for high test coverage** — consensus code is exercised by unit tests, integration tests, fuzzing, and (where applicable) BLVM Specification Lock; **CI does not enforce a single numeric coverage floor on every PR** (optional coverage workflows exist per repository). Add tests that cover new behavior and edge cases; follow each crate’s CI and `CONTRIBUTING` for what must pass before merge.

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

- **Match mainnet consensus rules** — no undocumented deviations in consensus code
- **Not deviate from the [Orange Paper](../reference/orange-paper.md) specifications** - Mathematical correctness required
- **Handle all edge cases correctly** - Consensus code must be bulletproof
- **Maintain mathematical precision** - No approximations

**Additional requirements**:
- **Dependencies**: Follow the canonical [`blvm-consensus` `Cargo.toml`](https://github.com/BTCDecoded/blvm-consensus/blob/main/Cargo.toml). Other **BLVM** crates are typically pulled with **pre-1.0 semver ranges** on crates.io; many **third-party** crates use **`=`** pins where listed. This is **not** “every dependency exact-pinned.”
- **Pure Functions**: All functions must remain side-effect-free
- **Testing**: All mathematical functions must be thoroughly tested (see [Testing Infrastructure](testing.md))
- **Formal Verification**: Consensus-critical changes may require Z3 proofs (via BLVM Specification Lock)

### blvm-protocol

- **Protocol Abstraction**: Changes must maintain clean abstraction
- **Variant Support**: Ensure all Bitcoin variants continue to work
- **Backward Compatibility**: Avoid breaking changes to protocol interfaces

### blvm-node

- **Consensus Integrity**: Never modify consensus rules (use blvm-consensus for that)
- **Production Readiness**: Consider production deployment implications
- **Performance**: Maintain reasonable performance characteristics
- **CI vs optional features**: Default **CI** usually matches **`cargo test`** with **default features**, not **`--all-features`**. Full feature matrices and large integration suites can be **much heavier** (compile time, RAM). See **[`blvm-node` CONTRIBUTING](https://github.com/BTCDecoded/blvm-node/blob/main/CONTRIBUTING.md)** (section on CI parity and optional features).

### Resource-intensive builds (any repository)

`cargo test --all-features`, broad integration tests, or large workspace builds can exceed the resource profile of default CI. Read the **target repository’s** **`CONTRIBUTING.md`** before assuming your laptop or CI tier is sufficient.

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

**Canonical review docs** (maintainer expectations vs AI “review intelligence”) live in the [governance](https://github.com/BTCDecoded/governance) repository; this book summarizes PR mechanics only. See [Review standards](../governance/overview.md#review-standards) in the Governance section for links.

### What Happens After You Submit a PR

1. **Automated CI runs** - Tests, linting, and checks run automatically
2. **Governance classification** — Your PR is assigned a **governance tier** and evaluated on a **repository layer**; effective rules combine both (see [Layer-Tier Model](../governance/layer-tier-model.md))
3. **Maintainers review** - Code review by project maintainers
4. **Signatures required** - Maintainers must cryptographically sign approval (see [PR Process](pr-process.md))
5. **Review period** — The effective **layer + tier** review period must elapse (see [PR Process](pr-process.md))
6. **Merge** - Once all requirements are met, your PR is merged

### Review Criteria

Reviewers will check:

- **Correctness** - Does the code work as intended?
- **Consensus compliance** — Does it match the Orange Paper and observed mainnet behavior? (for consensus code)
- **Test coverage** - Are all cases covered?
- **Performance** - No regressions?
- **Documentation** - Is it clear and complete?
- **Security** - Any potential vulnerabilities?

### Getting Your PR Reviewed

- **Be patient** — effective wait times follow **layer + tier** (see [Layer-Tier Model](../governance/layer-tier-model.md)); they are not always the tier-only numbers ([[gov:tier_1_review_days]]–[[gov:tier_5_review_days]] days).
- **Respond to feedback** - Address review comments promptly
- **Keep PRs small** - Smaller PRs are reviewed faster
- **Update PR description** - Keep it current as you make changes

## Governance tiers and review time

Your PR gets a **governance tier** (what kind of change) and applies on a **repository layer** (which repo). **Signature requirements and review clocks use the more restrictive of layer vs tier** (“most restrictive wins”). See [Layer-Tier Model](../governance/layer-tier-model.md) and [PR Process](pr-process.md).

The list below is **tier-only** review-period floors **when the repository layer does not impose something stricter** (the matrix in the Layer-Tier Model shows combined results—for example, **Tier 1** in **Layer 3** can still be **[[gov:matrix_3_1_review_days]] days**).

- **Tier 1: Routine maintenance** — bug fixes, documentation, performance optimizations in non-consensus areas; **[[gov:tier_1_review_days]] days** tier floor
- **Tier 2: Feature changes** — new RPC, P2P, wallet, SDK features; **[[gov:tier_2_review_days]] days** tier floor
- **Tier 3: Consensus-adjacent** — changes affecting consensus validation paths; **[[gov:tier_3_review_days]] days** tier floor
- **Tier 4: Emergency actions** — critical security / network-threatening PR path; **[[gov:tier_4_review_days]] days** once requirements met
- **Tier 5: Governance changes** — rules that change governance itself; **[[gov:tier_5_review_days]] days** tier floor

**Emergency response classes** (critical / urgent / elevated incidents, **[[gov:emergency_critical_activation]] keyholder activation**) are separate from these PR tiers; see [PR Process → Emergency Procedures](pr-process.md#emergency-procedures).

## Testing Your Changes

See [Testing Infrastructure](testing.md) for testing documentation. Key points:

- **Unit tests** - Test individual functions
- **Integration tests** - Test cross-module functionality
- **[Property-based testing](property-based-testing.md)** - Test with generated inputs
- **[Fuzzing](testing.md#fuzzing)** - Find edge cases automatically
- **[Differential testing](differential-testing.md)** — Cross-check vs Bitcoin Core (blvm-bench; full-chain program)

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
- **Security** — report to **security@thebitcoincommons.org** and follow **SECURITY.md** in the relevant repository for disclosure details

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

## Contributing to Documentation

For documentation-specific contributions (improving docs, fixing typos, adding examples), see [Contributing to Documentation](../appendices/contributing-docs.md). That page covers:

- Documentation standards and style guidelines
- Where to contribute (source repos vs. unified docs)
- Documentation workflow
- Local testing of documentation changes

**Note**: Code contributions (this page) and documentation contributions (linked above) follow different workflows but both are welcome!

## See Also

- [Repository layout](repository-architecture.md) - Why the codebase uses separate repositories and how local vs CI builds work
- [PR Process](pr-process.md) - Pull request review process and governance tiers
- [CI/CD Workflows](ci-cd-workflows.md) - What happens when you push code
- [Testing Infrastructure](testing.md) - Testing guides
- [Release Process](release-process.md) - How releases are created
- [Contributing to Documentation](../appendices/contributing-docs.md) - Documentation contribution guide

