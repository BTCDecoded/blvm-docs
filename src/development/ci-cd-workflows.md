# CI/CD Workflows

This document explains what happens when you push code or open a Pull Request, how to interpret CI results, and how to debug failures.

## Overview

BLVM uses GitHub Actions for continuous integration and deployment. All workflows run on **self-hosted Linux x64 runners** to ensure security and deterministic builds.

## What Happens When You Push Code

### On Push to Any Branch

When you push code to any branch, the following workflows may trigger:

1. **CI Workflow** - Runs tests, linting, and build verification
2. **Coverage Workflow** - Calculates test coverage
3. **Security Workflow** - Runs security checks (if configured)

### On Push to Main Branch

In addition to the above, pushing to `main` triggers:

1. **Release Workflow** - Automatically creates a new release (see [Release Process](release-process.md))
2. **Version Bumping** - Auto-increments patch version
3. **Cargo Publishing** - Publishes dependencies to crates.io
4. **Git Tagging** - Tags all repositories with the new version

## Repository-Specific CI Workflows

### blvm-consensus

**Workflows**:
- `ci.yml` - Runs test suite, linting, and build verification
- `coverage.yml` - Calculates test coverage

**What Runs**:
- Unit tests
- Integration tests
- Property-based tests
- BLVM Specification Lock formal verification (optional, can be enabled)
- Code formatting check (`cargo fmt --check`)
- Linting check (`cargo clippy`)

### blvm-protocol

**Workflows**:
- `ci.yml` - Runs test suite and build verification
- `coverage.yml` - Calculates test coverage

**What Runs**:
- Unit tests
- Integration tests
- Protocol compatibility tests
- Build verification

### blvm-node

**Workflows**:
- `ci.yml` - Runs test suite and build verification
- `coverage.yml` - Calculates test coverage

**What Runs**:
- Unit tests
- Integration tests
- Node functionality tests
- Network protocol tests
- Build verification

### blvm (Main Repository)

**Workflows**:
- `ci.yml` - Runs tests across all components
- `coverage.yml` - Aggregates coverage from all repos
- `release.yml` - Official release workflow
- `prerelease.yml` - Prerelease workflow
- `nightly-prerelease.yml` - Scheduled nightly builds

## Reusable Workflows (blvm-commons)

The `blvm-commons` repository provides reusable workflows that other repositories call:

### verify_consensus.yml

**Purpose**: Runs tests and optional BLVM Specification Lock verification for consensus code

**Inputs**:
- `repo` - Repository name
- `ref` - Git reference (branch/tag)
- `blvm-spec-lock` - Boolean to enable BLVM Specification Lock verification

**What It Does**:
- Checks out the repository
- Runs test suite
- Optionally runs BLVM Specification Lock formal verification
- Reports results

### build_lib.yml

**Purpose**: Deterministic library build with artifact hashing

**Inputs**:
- `repo` - Repository name
- `ref` - Git reference
- `package` - Cargo package name
- `features` - Feature flags to enable
- `verify_deterministic` - Optional: rebuild and compare hashes

**What It Does**:
- Builds the library with `cargo build --locked --release`
- Hashes outputs to `SHA256SUMS`
- Optionally verifies deterministic builds (rebuild and compare)

### build_docker.yml

**Purpose**: Builds Docker images

**Inputs**:
- `repo` - Repository name
- `ref` - Git reference
- `tag` - Docker image tag
- `image_name` - Docker image name
- `push` - Boolean to push to registry

**What It Does**:
- Builds Docker image
- Optionally pushes to registry

## Workflow Dependencies and Ordering

Builds follow a strict dependency order:

```
1. blvm-consensus (L2) - No dependencies
   ↓
2. blvm-protocol (L3) - Depends on blvm-consensus
   ↓
3. blvm-node (L4) - Depends on blvm-protocol + blvm-consensus
   ↓
4. blvm (main) - Depends on blvm-node

Parallel:
5. blvm-sdk - No dependencies
   ↓
6. blvm-commons - Depends on blvm-sdk
```

**Security Gates**: Consensus verification (tests + optional BLVM Specification Lock) must pass before downstream builds proceed.

## Self-Hosted Runners

All workflows run on **self-hosted Linux x64 runners**:

- **Security**: Code never leaves our infrastructure
- **Performance**: Faster builds, no rate limits
- **Deterministic**: Consistent build environment
- **Labels**: Optional labels (`rust`, `docker`, `blvm-spec-lock`) optimize job assignment (note: label uses lowercase for technical compatibility)

**Runner Policy**:
- All jobs run on `[self-hosted, linux, x64]` runners
- Workflows handle installation as fallback if labeled runners unavailable
- Repos should restrict Actions to self-hosted in settings

## Deterministic Builds

All builds use deterministic build practices:

- **Locked Dependencies**: `cargo build --locked` ensures exact dependency versions
- **Toolchain Pinning**: Per-repo `rust-toolchain.toml` defines exact Rust version
- **Artifact Hashing**: All outputs hashed to `SHA256SUMS`
- **Verification**: Optional deterministic verification (rebuild and compare hashes)

## Interpreting CI Results

### ✅ Success

All checks pass:
- ✅ Tests pass
- ✅ Linting passes
- ✅ Build succeeds
- ✅ Coverage meets threshold

**Action**: Your PR is ready for review (subject to governance requirements).

### ❌ Test Failures

One or more tests fail:
- Check the test output in the workflow logs
- Look for error messages and stack traces
- Run tests locally to reproduce: `cargo test`

**Common Causes**:
- Logic errors in your code
- Test environment differences
- Flaky tests (timing issues)

### ❌ Linting Failures

Code style or quality issues:
- **Formatting**: Run `cargo fmt` locally
- **Clippy warnings**: Run `cargo clippy -- -D warnings` and fix issues

**Action**: Fix locally and push again.

### ❌ Build Failures

Code doesn't compile:
- Check compiler errors in workflow logs
- Build locally: `cargo build`
- Check for missing dependencies or version conflicts

**Action**: Fix compilation errors and push again.

### ⚠️ Coverage Below Threshold

Test coverage is below the required threshold:
- Add more tests to cover untested code
- Check coverage report to see what's missing

**Action**: Add tests to increase coverage.

## Debugging CI Failures

### 1. Check Workflow Logs

Click on the failed check in your PR to see detailed logs:
- Expand failed job
- Look for error messages
- Check which step failed

### 2. Reproduce Locally

Run the same commands locally:

```bash
# Run tests
cargo test

# Check formatting
cargo fmt --check

# Run clippy
cargo clippy -- -D warnings

# Build
cargo build --release
```

### 3. Check for Environment Differences

CI runs in a clean environment:
- Dependencies are fresh
- No local configuration
- Specific Rust toolchain version

**Solution**: Use `rust-toolchain.toml` to pin Rust version.

### 4. Common Issues

**Issue**: Tests pass locally but fail in CI
- **Cause**: Timing issues, environment differences
- **Solution**: Make tests more robust, check for race conditions

**Issue**: Build works locally but fails in CI
- **Cause**: Dependency version mismatch
- **Solution**: Ensure `Cargo.lock` is committed, use `--locked` flag

**Issue**: Coverage calculation fails
- **Cause**: Coverage tool issues
- **Solution**: Check coverage tool version, ensure tests run successfully

## Workflow Status Checks

PRs require all status checks to pass before merging:

- **Required Checks**: Must pass (configured per repository)
- **Optional Checks**: Can fail but won't block merge
- **Status**: Shown in PR checks section

**Note**: Even if all checks pass, PRs still require:
- Maintainer signatures (see [PR Process](pr-process.md))
- Review period to elapse

## Best Practices

### Before Pushing

1. **Run tests locally**: `cargo test`
2. **Check formatting**: `cargo fmt`
3. **Run clippy**: `cargo clippy -- -D warnings`
4. **Build**: `cargo build --release`

### During Development

1. **Push frequently**: Small commits are easier to debug
2. **Check CI early**: Don't wait until PR is "done"
3. **Fix issues immediately**: Don't let failures accumulate

### When CI Fails

1. **Don't panic**: CI failures are normal during development
2. **Read the logs**: Error messages are usually clear
3. **Reproduce locally**: Fix the issue, then push again
4. **Ask for help**: If stuck, ask in discussions or PR comments

## Workflow Configuration

Workflows are configured in `.github/workflows/` in each repository:

- **Trigger conditions**: When workflows run
- **Job definitions**: What each job does
- **Runner requirements**: Which runners to use
- **Dependencies**: Job ordering

**Note**: Workflows in `blvm-commons` are reusable and called by other repositories via `workflow_call`.

## Workflow Optimization

### Caching Strategies

For self-hosted runners, local caching can provide significant performance improvements:

#### Local Caching System

Using `/tmp/runner-cache` with rsync provides 10-100x faster cache operations than GitHub Actions cache:

- **No API rate limits**: Local filesystem access
- **Faster restore**: rsync is much faster than GitHub cache API
- **Works offline**: Once cached, no network needed
- **Preserves symlinks**: Better than GitHub cache for complex builds

#### Shared Setup Jobs

Use a single setup job that all other jobs depend on:

- **Checkout dependencies once**: Avoid redundant checkouts
- **Generate cache keys once**: Share keys via job outputs
- **Parallel execution**: Other jobs can run in parallel after setup

#### Cross-Repo Build Artifact Caching

Cache `target/` directories for dependencies across workflow runs:

- **Don't rebuild dependencies**: Cache blvm-consensus and blvm-protocol build artifacts
- **Faster incremental builds**: Only rebuild what changed
- **Shared across repos**: Same cache can be used by multiple repositories

#### Cache Key Strategy

Use deterministic cache keys based on:
- `Cargo.lock` hash (for dependency changes)
- Rust toolchain version (for toolchain changes)
- Combined key: `${DEPS_KEY}-${TOOLCHAIN}`

#### Disk Space Management

For long-running runners, implement cache cleanup:

- **Automatic cleanup**: Remove caches older than N days
- **Keep recent caches**: Maintain last N cache entries
- **Emergency cleanup**: Check disk space and clean if >80% full

### Performance Improvements

With proper caching optimization:
- **Dependency checkout**: ~30s (once in setup job)
- **Cache restore**: ~5s per job (local cache vs ~20s for GitHub cache)
- **Dependency build**: ~30s (cached artifacts vs ~5min without cache)
- **Total overhead**: ~2min vs ~35min without optimization

**Estimated speedup**: ~17x faster for setup overhead

## Additional Resources

- [Testing Infrastructure](testing.md) - Comprehensive testing documentation
- [Release Process](release-process.md) - How releases are created
- [PR Process](pr-process.md) - Pull request review process

