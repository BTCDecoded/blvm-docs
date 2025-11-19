# Deployment Optimization Plan

## Current Status Assessment

### ✅ What's Ready
1. **Core Bitcoin Node**: Fully functional, consensus-compliant
2. **Release Pipeline**: `release.yml` works and creates GitHub releases
3. **Cross-Repo Orchestration**: `release_orchestrator.yml` coordinates builds
4. **Infrastructure**: GitHub runners and GitHub App available

### ⚠️ What's Blocking Deployment

#### 1. **Governance App Not Deployed** (P0)
- **Status**: Code complete but not running
- **Impact**: No automated governance enforcement
- **Solution**: Deploy governance app (see below)

#### 2. **Placeholder Keys** (P0)
- **Status**: All maintainer keys are placeholders
- **Impact**: No real cryptographic security
- **Solution**: Key ceremony to generate real keys

#### 3. **Database Queries Not Implemented** (P0)
- **Status**: Governance app database functions return empty
- **Impact**: No persistence of governance data
- **Solution**: Implement SQLite/PostgreSQL queries

#### 4. **Not Battle-Tested** (P1)
- **Status**: No production deployment yet
- **Impact**: Unknown edge cases, performance under load
- **Solution**: Gradual rollout (testnet → mainnet beta → production)

## Deployment Strategy

### Phase 1: Prerelease (Current)
**Goal**: Validate release pipeline, create prerelease artifacts

**Actions**:
1. ✅ Move `release.yml` → `prerelease.yml` (done)
2. Create `release.yml` that calls prerelease + additional checks
3. Tag releases as `v0.1.0-prerelease.1`, `v0.1.0-prerelease.2`, etc.
4. Test cross-repo release pipeline

### Phase 2: Testnet Deployment
**Goal**: Deploy to Bitcoin testnet, validate in real network

**Actions**:
1. Deploy governance app (dry-run mode)
2. Run node on testnet for 1-2 weeks
3. Monitor performance, stability, consensus compliance
4. Fix any issues discovered

### Phase 3: Mainnet Beta
**Goal**: Limited mainnet deployment with trusted users

**Actions**:
1. Deploy governance app (enforcement mode)
2. Generate real cryptographic keys
3. Limited mainnet deployment (10-20 nodes)
4. Monitor for 1 month

### Phase 4: Production
**Goal**: Full public release

**Actions**:
1. Complete security audit
2. Full documentation
3. Public announcement
4. Open to all users

## Release Pipeline Optimization

### ⚠️ Current State: Duplication Identified

**We have THREE systems doing similar things:**

1. **GitHub Actions Workflow** (`release_orchestrator.yml`)
   - Uses workflow dependencies
   - Already working
   - Complex, hard to maintain

2. **Bash Scripts** (`build-release-chain.sh`, `build.sh`)
   - Good for local development
   - Manual execution
   - No monitoring

3. **Rust (Governance App)** - NEW
   - Centralized orchestration
   - Better error handling
   - State persistence
   - Webhook-driven

**See**: `RELEASE_ORCHESTRATION_CONSOLIDATION.md` for consolidation plan

### Recommended Architecture: Governance App Orchestration (Consolidated)

**Key Insight**: The governance app is already a GitHub App with full API access. It can handle cross-repo orchestration!

```
Release Trigger (GitHub Release event or manual)
  ↓
Governance App (webhook handler)
  ├── Receives release event
  ├── Determines build order from dependency graph
  ├── Triggers workflows via repository_dispatch
  ├── Monitors build status via GitHub API
  ├── Handles retries and error recovery
  ├── Coordinates artifact collection
  └── Creates unified release

Individual Repo Workflows (simplified)
  ├── build.yml (triggered by repository_dispatch)
  │   ├── Build artifacts
  │   ├── Run tests
  │   └── Post status back to governance app
  └── verify.yml (existing verification)
```

**Benefits**:
- ✅ Centralized orchestration logic
- ✅ Better error handling and retries
- ✅ Visibility into entire build pipeline
- ✅ Can pause/resume builds
- ✅ Can handle complex dependency graphs
- ✅ Single source of truth for build state
- ✅ Leverages existing GitHub App permissions

### Simplified Workflow Files

Each repo only needs simple build workflows:

```yaml
# .github/workflows/build.yml (in each repo)
name: Build

on:
  repository_dispatch:
    types: [build-request]

jobs:
  build:
    runs-on: [self-hosted, Linux, X64]
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: cargo build --release
      - name: Post status
        uses: actions/github-script@v7
        with:
          script: |
            // Post status back to governance app
            await github.rest.repos.createDispatchEvent({
              owner: 'BTCDecoded',
              repo: 'governance-app',
              event_type: 'build-complete',
              client_payload: {
                repo: context.repo.repo,
                status: 'success',
                artifacts: [...]
              }
            })
```

### Governance App Build Orchestration Module

Add to governance app:

```rust
// governance-app/src/build/orchestrator.rs

pub struct BuildOrchestrator {
    github_client: GitHubClient,
    database: Database,
}

impl BuildOrchestrator {
    /// Handle release event and orchestrate builds
    pub async fn handle_release_event(&self, payload: &Value) -> Result<()> {
        let version = extract_version(payload)?;
        let repos = self.get_build_order()?; // From dependency graph
        
        // Start builds in parallel where possible
        for repo in repos {
            self.trigger_build(&repo, &version).await?;
        }
        
        // Monitor builds
        self.monitor_builds(version).await?;
        
        // Collect artifacts
        self.collect_artifacts(version).await?;
        
        // Create unified release
        self.create_unified_release(version).await?;
    }
    
    /// Trigger build for a specific repo
    async fn trigger_build(&self, repo: &str, version: &str) -> Result<()> {
        self.github_client
            .repos(owner, repo)
            .create_dispatch_event("build-request", json!({
                "version": version,
                "triggered_by": "governance-app"
            }))
            .await?;
    }
    
    /// Monitor build status across all repos
    async fn monitor_builds(&self, version: &str) -> Result<()> {
        // Poll GitHub API for workflow status
        // Handle failures, retries, timeouts
        // Update database with build state
    }
}
```

### GitHub Release Integration

**Yes, using GitHub Releases is proper!** Here's why:

1. **Standard Practice**: GitHub Releases are the standard for distributing binaries
2. **Artifact Storage**: GitHub stores release artifacts automatically
3. **Versioning**: Tags provide clear versioning
4. **Webhooks**: Release events can trigger downstream workflows
5. **Verification**: SHA256SUMS can be attached to releases

### Recommended Workflow

```yaml
# .github/workflows/release.yml (commons repo)
name: Production Release

on:
  workflow_dispatch:
    inputs:
      version_tag:
        description: 'Version tag (e.g., v0.1.0)'
        required: true
        type: string
      prerelease:
        description: 'Mark as prerelease?'
        required: false
        default: 'false'
        type: boolean

jobs:
  prerelease:
    uses: ./.github/workflows/prerelease.yml
    with:
      version_tag: ${{ inputs.version_tag }}
      prerelease: ${{ inputs.prerelease }}
  
  security-checks:
    needs: prerelease
    runs-on: ubuntu-latest
    steps:
      - name: Verify signatures
      - name: Check for known vulnerabilities
      - name: Verify deterministic builds
  
  create-release:
    needs: [prerelease, security-checks]
    uses: softprops/action-gh-release@v1
    with:
      prerelease: ${{ inputs.prerelease }}
```

## Governance App Deployment

### Should You Deploy It?

**YES, but in stages:**

1. **Phase 1 (Now)**: Deploy in **dry-run mode**
   - Logs all governance decisions
   - Does NOT block merges
   - Validates the system works
   - No risk to development workflow

2. **Phase 2 (After 1-2 weeks)**: Deploy in **enforcement mode**
   - Actually blocks merges
   - Requires real keys
   - Full governance enforcement

### Deployment Steps

#### 1. Deploy Governance App (Dry-Run)

```bash
# On your GitHub runner or dedicated server
cd governance-app

# Set environment variables
export DRY_RUN_MODE=true
export GITHUB_APP_ID=your_app_id
export GITHUB_PRIVATE_KEY_PATH=/path/to/key.pem
export GITHUB_WEBHOOK_SECRET=your_secret
export DATABASE_URL=sqlite:governance.db

# Run migrations
cargo run --bin governance-app -- migrate

# Start app (or use systemd)
cargo run --bin governance-app
```

#### 2. Install GitHub App

1. Go to GitHub Settings → Developer settings → GitHub Apps
2. Create new app or use existing
3. Set webhook URL to your server
4. Install on BTCDecoded organization
5. Grant permissions:
   - Contents: Read
   - Pull requests: Write
   - Statuses: Write

#### 3. Configure GitHub Actions Integration

```yaml
# .github/workflows/governance-check.yml
name: Governance Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  governance-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check governance rules
        uses: actions/github-script@v7
        with:
          script: |
            // Governance app will post status check
            // This workflow just ensures it's triggered
```

## GitHub Runners + GitHub App Integration

### Architecture: Unified Governance App

```
GitHub Event (PR opened, Release created, etc.)
  ↓
GitHub App (webhook)
  ↓
Governance App Server (Single Point of Control)
  ├── Governance Enforcement
  │   ├── Validates governance rules
  │   ├── Posts status checks
  │   └── Blocks merges if needed
  ├── Build Orchestration
  │   ├── Triggers cross-repo builds
  │   ├── Monitors build status
  │   ├── Handles retries/errors
  │   └── Coordinates artifact collection
  └── Release Management
      ├── Creates unified releases
      ├── Verifies artifacts
      └── Publishes to GitHub Releases
  ↓
GitHub Actions (Simple Build Workers)
  ├── Receives build requests via repository_dispatch
  ├── Runs build/test
  └── Posts status back to governance app
```

### Setup

1. **Governance App** (central orchestrator)
   - Deployed on your server
   - Receives ALL webhooks from GitHub
   - Handles governance + builds + releases
   - Uses GitHub App API for all operations

2. **GitHub Actions** (simple workers)
   - Minimal workflow files
   - Just build/test on demand
   - Report status back to governance app

### Governance App Permissions Needed

Add to GitHub App permissions:
- **Repository permissions**:
  - Contents: Read/Write (for artifacts)
  - Actions: Read/Write (to trigger workflows)
  - Pull requests: Write (status checks)
  - Statuses: Write
  - Releases: Write (create releases)
- **Subscribe to events**:
  - Pull request
  - Release
  - Workflow run (to monitor builds)
  - Repository dispatch (to receive build status)

### Recommended Setup

```yaml
# governance-app config
[github]
app_id = "123456"
private_key_path = "/etc/governance/github-app.pem"
webhook_secret = "your_secret"
dry_run = true  # Start with dry-run

[server]
host = "0.0.0.0"
port = 8080

[database]
url = "sqlite:governance.db"  # Or PostgreSQL for production
```

## Optimization Checklist

### Immediate (This Week)

- [ ] Move `release.yml` → `prerelease.yml` ✅ (done)
- [ ] Create new `release.yml` that calls prerelease + security checks
- [ ] **Add build orchestration module to governance app** ✅ (done)
  - [x] Implement `BuildOrchestrator` struct
  - [x] Add dependency graph configuration
  - [x] Implement build triggering via `repository_dispatch`
  - [x] Implement build monitoring via GitHub API (partial)
  - [x] Add artifact collection logic (structure ready)
- [ ] **Testing Strategy** (CRITICAL - Prove It Works)
  - [ ] Create comprehensive test suite (see `governance-app/PROOF_OF_WORK_TESTING.md`)
  - [ ] Add unit tests for build orchestration ✅ (started)
  - [ ] Add integration tests with mocks
  - [ ] Run E2E test with test release
  - [ ] Run comparison test (both systems on same release)
  - [ ] Test failure scenarios
- [ ] **Prove It Works** (2-3 weeks)
  - [ ] All unit tests pass
  - [ ] All integration tests pass
  - [ ] E2E test successful
  - [ ] Comparison test shows identical results
  - [ ] Failure scenarios handled correctly
- [ ] **Consolidate orchestration systems** (After Proof)
  - [ ] Switch governance app to primary
  - [ ] Keep workflow orchestrator as fallback
  - [ ] Monitor for 1-2 releases
  - [ ] Then mark `release_orchestrator.yml` as deprecated
  - [ ] Add fallback to workflow orchestrator in governance app
  - [ ] Keep bash scripts for local development only
  - [ ] Document consolidation plan
- [ ] **Complete governance app implementation**
  - [ ] Implement workflow run ID retrieval
  - [ ] Complete build monitoring
  - [ ] Complete artifact collection
  - [ ] Complete release creation
- [ ] **Simplify repo workflows**
  - [ ] Create simple `build.yml` in each repo (triggered by repository_dispatch)
  - [ ] Remove complex orchestration from workflows
- [ ] Test cross-repo release pipeline end-to-end
- [ ] Deploy governance app in dry-run mode
- [ ] Install GitHub App on organization (with Actions permissions)
- [ ] Test webhook delivery

### Short-term (Next 2 Weeks)

- [ ] Implement database queries in governance app
- [ ] Generate real cryptographic keys (key ceremony)
- [ ] Deploy node to testnet
- [ ] Monitor testnet deployment
- [ ] Create deployment runbook

### Medium-term (Next Month)

- [ ] Security audit of consensus layer
- [ ] Performance benchmarking
- [ ] Load testing
- [ ] Documentation completion
- [ ] Community announcement

## Release Pipeline Best Practices

### 1. Version Tagging

```bash
# Prerelease
v0.1.0-prerelease.1
v0.1.0-prerelease.2

# Release candidate
v0.1.0-rc.1
v0.1.0-rc.2

# Production
v0.1.0
v0.1.1  # Patch
v0.2.0  # Minor
v1.0.0  # Major
```

### 2. Release Artifacts

Each release should include:
- Binaries (Linux, Windows, macOS)
- SHA256SUMS file
- SHA256SUMS.asc (GPG signature)
- Release notes
- Verification bundle (Kani proofs, test results)

### 3. Deterministic Builds

```yaml
- name: Verify deterministic build
  run: |
    # Build twice, compare hashes
    cargo build --release
    HASH1=$(sha256sum target/release/bllvm)
    cargo clean
    cargo build --release
    HASH2=$(sha256sum target/release/bllvm)
    if [ "$HASH1" != "$HASH2" ]; then
      echo "Build is not deterministic!"
      exit 1
    fi
```

### 4. Cross-Repo Coordination (via Governance App)

The governance app handles all cross-repo coordination:

```rust
// governance-app/src/build/orchestrator.rs

// Dependency graph (can be in config or database)
const BUILD_ORDER: &[(&str, &[&str])] = &[
    ("bllvm-consensus", &[]),
    ("bllvm-protocol", &["bllvm-consensus"]),
    ("bllvm-node", &["bllvm-protocol", "bllvm-consensus"]),
    ("bllvm-sdk", &["bllvm-node"]),
    ("bllvm", &["bllvm-node"]),
];

impl BuildOrchestrator {
    /// Get build order respecting dependencies
    fn get_build_order(&self) -> Vec<String> {
        // Topological sort of dependency graph
        // Returns: ["bllvm-consensus", "bllvm-protocol", "bllvm-node", ...]
    }
    
    /// Trigger builds in parallel where dependencies allow
    async fn trigger_builds(&self, version: &str) -> Result<()> {
        let order = self.get_build_order();
        let mut completed = HashSet::new();
        
        for repo in order {
            // Wait for dependencies
            let deps = self.get_dependencies(repo)?;
            for dep in deps {
                self.wait_for_build(&dep, version).await?;
            }
            
            // Trigger this build
            self.trigger_build(repo, version).await?;
            completed.insert(repo);
        }
    }
}
```

**Benefits**:
- ✅ Single source of truth for build dependencies
- ✅ Automatic parallelization where possible
- ✅ Better error handling and retries
- ✅ Can pause/resume entire pipeline
- ✅ Centralized logging and monitoring

## Security Considerations

### Before Production

1. **Key Management**
   - Generate real keys via key ceremony
   - Store keys securely (HSM, key management service)
   - Implement key rotation

2. **Access Control**
   - Limit who can trigger releases
   - Require approvals for production releases
   - Audit all release actions

3. **Verification**
   - Verify all binaries before release
   - Sign releases with GPG
   - Provide verification instructions

## Monitoring

### What to Monitor

1. **Release Pipeline**
   - Build success rate
   - Build duration
   - Artifact sizes
   - Test pass rate

2. **Governance App**
   - Webhook delivery success
   - Status check posting
   - Database query performance
   - Error rates

3. **Node Deployment**
   - Uptime
   - Consensus compliance
   - Network connectivity
   - Resource usage

## Next Steps

1. **This Week**:
   - ✅ Test prerelease pipeline
   - **Add build orchestration to governance app** (NEW)
   - Deploy governance app (dry-run)
   - Document deployment process

2. **Next Week**:
   - Implement database queries
   - Generate real keys
   - Test build orchestration end-to-end
   - Deploy to testnet

3. **Next Month**:
   - Security audit
   - Performance testing
   - Public beta announcement

## Governance App Build Orchestration Implementation

### New Module Structure

```
governance-app/src/
  ├── build/
  │   ├── mod.rs
  │   ├── orchestrator.rs      # Main orchestration logic
  │   ├── dependency.rs        # Dependency graph management
  │   ├── monitor.rs           # Build status monitoring
  │   └── artifacts.rs         # Artifact collection
  └── webhooks/
      └── release.rs           # Handle release events
```

### Implementation Priority

1. **Phase 1**: Basic orchestration
   - Trigger builds via `repository_dispatch`
   - Monitor build status
   - Handle simple dependency chain

2. **Phase 2**: Advanced features
   - Parallel builds where possible
   - Retry logic
   - Artifact collection
   - Unified release creation

3. **Phase 3**: Production features
   - Build caching
   - Performance optimization
   - Advanced error recovery
   - Build analytics

---

**Remember**: Start small, validate incrementally, scale gradually. The core Bitcoin implementation is solid - now it's about operational excellence.

