# Release Process

## Overview

BLVM uses an automated release pipeline that builds and releases the entire ecosystem when code is merged to `main` in any repository. The system uses Cargo's dependency management to build repositories in the correct order.

## Release Triggers

### Automatic Release (Push to Main)

The release pipeline automatically triggers when:

- A commit is pushed to the `main` branch in any repository
- The commit changes code files (not just documentation)
- **Paths ignored**: markdown files, `.github/**`, `docs/**`

**What happens**:
1. Version is auto-incremented (patch version: X.Y.Z → X.Y.(Z+1))
2. Dependencies are published to crates.io
3. All repositories are built in dependency order
4. Release artifacts are created
5. GitHub release is created
6. All repositories are tagged with the version

### Manual Release (Workflow Dispatch)

You can manually trigger a release with:

- **Custom version tag** (e.g., `v0.2.0`)
- **Platform selection** (linux, windows, or both)
- **Option to skip tagging** (for testing)

**When to use**:
- Major or minor version bumps
- Coordinated releases
- Testing release process

## Version Numbering

### Automatic Version Bumping

When triggered by a push to `main`:

1. Reads current version from `blvm/versions.toml` (from `blvm-consensus` version)
2. Auto-increments the patch version (X.Y.Z → X.Y.(Z+1))
3. Generates a release set ID (e.g., `set-2025-0123`)

### Manual Version Override

When using workflow dispatch:

- Provide a specific version tag (e.g., `v0.2.0`)
- The pipeline uses your provided version instead of auto-incrementing

### Semantic Versioning

BLVM uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

## Release notes: deployment maturity (**D4**)

Operator-facing artifacts should include **one sentence** pointing at **[Deployment posture](https://docs.thebitcoincommons.org/security/deployment-posture.html)** (RPC exposure, QUIC × auth limits) and **[RPC transport × authentication](https://docs.thebitcoincommons.org/security/rpc-transport-auth-matrix.html)**.

Example:

> Operators remain responsible for `[rpc_auth]` on non-loopback RPC; QUIC JSON-RPC uses HTTP/3 and shares the Bearer/`RpcAuthManager` contract with TCP HTTP: still treat the UDP QUIC listener as its own exposure surface. See Deployment posture and RPC transport × authentication in the BLVM docs.

## Build Process

### Dependency Order

Publishing and local builds follow each crate’s **Cargo** dependency graph (not a single linear list). In practice:

- **Foundation**: **blvm-primitives** is shared by **blvm-consensus** and **blvm-protocol**.
- **Core node path**: **blvm-consensus** → **blvm-protocol** → **blvm-node** → **`blvm`** CLI binary (the `blvm` crate depends on `blvm-node`).
- **SDK / governance**: **blvm-sdk** depends on **blvm-protocol** and **blvm-consensus** (and optionally **blvm-node** via features). **blvm-commons** depends on **blvm-sdk** and **blvm-protocol**.

So `blvm-sdk` is **not** a leaf with “no dependencies”; it sits beside the node stack and pulls protocol/consensus crates.

### Build Variants

Stable **GitHub Releases** ship one **base** binary set per tag (see [Release artifacts](#release-artifacts)). Experimental compile-time features are **not** published as separate release tarballs on every stable tag.

#### Base variant (stable releases)

**Purpose**: Default binaries on GitHub Releases and GHCR stable tags.

**Cargo features** (platform-specific: see CI `ci.yml`):

| Platform | Build command (summary) | Feature set |
|----------|-------------------------|-------------|
| **Linux x86_64** | `cargo build --release` | `blvm` **default** features (see `blvm/Cargo.toml`; `rocksdb` optional, not in defaults) |
| **Linux aarch64** | Cross-build via `scripts/ci-build-aarch64.sh` | Same as Linux x86_64 (`BLVM_LINUX_RELEASE_FEATURES` in `scripts/ci-portable-cross-features.sh`) |
| **Windows x86_64** | Cross-build, `--no-default-features` | Linux defaults minus Unix-only `nix` / `libc` (`BLVM_PORTABLE_CROSS_FEATURES`) |

Core P2P, RPC, storage, modules, **iroh**, **dandelion**, **sigop**, **governance**, **REST `/api/v1/*`**, **BIP70 payment RPC**, and **storage/index zstd compression** are in the shared release feature set on all platforms. Runtime compression stays **off** until configured (`[storage.compression]` or `storage.indexing.enable_compression`). **RocksDB** remains opt-in (`--features rocksdb`). Other extras (CTV, Stratum V2, …) still require explicit `--features` or the [experimental CI bundle](#experimental-variant-source-build) when not in your binary.

#### Experimental variant (source build)

**Purpose**: Optional features enabled at compile time (release CI uses `production,utxo-commitments,ctv,dandelion,stratum-v2,sigop,iroh`; local builds may use `--all-features` or pick features).

**Features** (experimental / non-base release build):

- UTXO commitments
- Dandelion++ privacy relay
- BIP119 CheckTemplateVerify (CTV)
- Stratum V2 mining integration
- Signature operations counting
- Iroh transport support

**BIP158** compact block filter support is included in default builds as well (CLI/ENV preference flags; no separate `bip158` Cargo feature on the default release binary).

**Use for**: Development, testing, and operators who compile locally.

See [Installation: Experimental build variant](../getting-started/installation.md#experimental-variant).

### Platforms

Stable release artifacts include:

- **Linux x86_64**: `.deb`, `.rpm`, Arch `.pkg.tar.gz`, standalone binary, `.tar.gz`
- **Linux aarch64**: standalone binary, `.tar.gz`
- **Windows x86_64**: portable `.exe`, `.zip` (MinGW `gnu` target)

Rolling **nightly** binaries and `ghcr.io/btcdecoded/blvm:nightly` are published from the `develop` branch (see [Release channels](#release-channels)).

## Release Artifacts

### Binaries Included

Stable release archives include:

- `blvm` - Bitcoin reference node
- `blvm-keygen` - Key generation tool
- `blvm-sign` - Message signing tool
- `blvm-verify` - Signature verification tool
- `blvm-commons` - Governance application server (Linux only)
- `key-manager` - Key management utility
- `test-content-hash` - Content hash testing tool
- `test-content-hash-standalone` - Standalone content hash test

### Archive Formats

Each release tag produces platform archives (Linux `.tar.gz`, Windows `.zip`, plus checksum files). Download matrix: **[btcdecoded.org/install](https://btcdecoded.org/install)**. Platform/feature notes: [Installation](../getting-started/installation.md#platform-feature-notes).

### Release Notes

Automatically generated release notes includes:

- Release date
- Component versions
- Build variant descriptions
- Installation instructions
- Verification instructions

## Quality Assurance

### Deterministic Build Verification

The pipeline verifies builds are reproducible by:

1. Building once and saving binary hashes
2. Cleaning and rebuilding
3. Comparing hashes (must match exactly)

**Note**: Non-deterministic builds are warnings (not failures) but should be fixed for production.

### Test Execution

All repositories run their test suites:

- Unit tests
- Integration tests
- Library and binary tests
- **Excluded**: Doctests (for build speed)

**Test Requirements**:
- All tests must pass
- 30-minute timeout per repository
- Single-threaded execution to avoid resource contention

## Release channels

| Channel | Source | Artifacts | crates.io |
|---------|--------|-----------|-----------|
| **Stable** | `main` release job | Versioned GitHub Release + `ghcr.io/btcdecoded/blvm:{version}` | Stable crate versions |
| **Develop / nightly** | `develop` branch | Rolling `nightly` tag, `ghcr.io/btcdecoded/blvm:nightly` | Coordinated pre-release set when published |

Stable releases trigger `repository_dispatch(blvm-release)` on **`website`** and **`commons-website`** so [btcdecoded.org/install](https://btcdecoded.org/install) picks up new artifacts. The **`blvm-docs`** book points there for downloads and does not redeploy on each **`blvm`** tag.

## Git Tagging

### Automatic Tagging

When a release succeeds, the pipeline:

1. Creates git tags in all repositories with the version tag
2. Tags are annotated with release message
3. Pushes tags to origin

**Repositories Tagged**:
- `blvm-consensus`
- `blvm-protocol`
- `blvm-node`
- `blvm`
- `blvm-sdk`
- `blvm-commons`

### Tag Format

- **Format**: `vX.Y.Z` (e.g., `v0.1.0`)
- **Semantic versioning**
- **Immutable** once created

## GitHub Release

### Release Creation

The pipeline creates a GitHub release with:

- **Tag**: Version tag (e.g., `v0.1.0`)
- **Title**: `Bitcoin Commons v0.1.0`
- **Body**: Generated from release notes
- **Artifacts**: All binary archives and checksums
- **Type**: Official release (not prerelease)

### Release Location

Releases are created in the `blvm` repository as the primary release point for the ecosystem.

## Cargo Publishing

### Publishing Strategy

To avoid compiling all dependencies when building the final `blvm` binary, all library dependencies are published to [crates.io](https://crates.io) as part of the release process.

**Publishing Order** (respect Cargo edges; automation can batch steps):

1. **blvm-primitives** (shared foundation)
2. **blvm-consensus** (depends on primitives)
3. **blvm-protocol** (depends on consensus + primitives)
4. **blvm-node** (depends on protocol + consensus)
5. **blvm-sdk** (depends on protocol + consensus; optional **blvm-node** via features), **not** independent of the consensus stack
6. **blvm-commons** (depends on sdk + protocol)
7. **`blvm`** binary crate (depends on **blvm-node**) when publishing the CLI

### Publishing Process

The release pipeline automatically:

1. **Publishes dependencies** in dependency order to crates.io
2. **Waits for publication** to complete before building dependents
3. **Updates Cargo.toml** in dependent repos to use published versions
4. **Builds final binary** using published crates (no compilation of dependencies)

### Benefits

- **Faster builds**: Final binary uses pre-built dependencies
- **Better caching**: Cargo can cache published crates
- **Version control**: Exact versions published and tracked
- **Reproducibility**: Same versions available to all users
- **Distribution**: Users can depend on published crates directly

### Crate Names

Published crates use the same names as the repositories:
- `blvm-consensus` → `blvm-consensus`
- `blvm-protocol` → `blvm-protocol`
- `blvm-node` → `blvm-node`
- `blvm-sdk` → `blvm-sdk`

## Version Coordination

### versions.toml

The `blvm/versions.toml` file tracks:

- Current version of each repository
- Dependency requirements
- Release set ID

### Updating Versions

**For major/minor version bumps**:
1. Manually edit `versions.toml`
2. Update version numbers
3. Trigger release with workflow dispatch
4. Provide the new version tag

**For patch releases**:
- Automatic via push to main
- Patch version auto-increments

## Release Verification

### Verifying Release Artifacts

1. **Download artifacts** from GitHub release
2. **Download SHA256SUMS** file
3. **Verify checksums**:
 ```bash
 sha256sum -c SHA256SUMS
 ```
4. **Verify signatures** (if GPG signing is enabled)

### Verifying Deterministic Builds

For deterministic build verification:

1. Check release notes for deterministic build status
2. Compare hashes from multiple builds (if available)
3. Rebuild from source and compare hashes

## Getting Notified of Releases

### GitHub Notifications

- **Watch repository**: Get notified of all releases
- **Release notifications**: GitHub will notify you of new releases

### Release Announcements

Announce releases through:
- GitHub release notes
- Project website
- Community channels (if configured)

## Best Practices

### When to Release

- **Automatic**: After merging PRs to main (recommended)
- **Manual**: For major/minor version bumps
- **Skip**: For documentation-only changes (auto-ignored)

### Version Strategy

- **Patch**: Bug fixes, minor improvements (auto-increment)
- **Minor**: New features, backward compatible (manual)
- **Major**: Breaking changes (manual)

### Release Frequency

- **Regular**: After each merge to main (automatic)
- **Scheduled**: For coordinated releases (manual)
- **Emergency**: For critical fixes (manual with version override)

## Troubleshooting

### Build Failures

**Common Issues**:
- Missing dependencies: Check all repos are cloned
- Cargo config issues: Pipeline auto-fixes common problems
- Windows cross-compile: Verify MinGW is installed

**Solutions**:
- Check build logs in GitHub Actions
- Verify all repositories are accessible
- Ensure Rust toolchain is up to date

### Test Failures

**Common Issues**:
- Flaky tests: Check for timing issues
- Resource contention: Tests run single-threaded
- Timeout: Tests have 30-minute limit

**Solutions**:
- Review test output in logs
- Check for CI-specific test issues
- Consider skipping problematic tests temporarily

### Tagging Failures

**Common Issues**:
- Tag already exists: Pipeline skips gracefully
- Permission issues: Verify `REPO_ACCESS_TOKEN` has write access

**Solutions**:
- Check if tag exists before release
- Verify token permissions
- Use `skip_tagging` option for testing

## Upgrading an existing deployment {#upgrading-an-existing-deployment}

Before upgrading, read [GitHub Releases](https://github.com/BTCDecoded/blvm/releases) for breaking config, storage, or RPC changes. Stop the node, back up the datadir, then replace the binary: see [Node Operations: Updates](../node/operations.md#updates).

## Additional Resources

- [CI/CD Workflows](ci-cd-workflows.md) - Detailed CI/CD documentation
- [Contributing Guide](contributing.md) - Developer workflow
- [GitHub Releases](https://github.com/BTCDecoded/blvm/releases) - All releases

