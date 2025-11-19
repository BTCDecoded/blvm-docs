# Documentation Organization Plan

## Overview
Organize documentation files across BTCDecoded **git repositories** to improve maintainability and discoverability.

**Note**: BTCDecoded root directory is NOT a git repository, so files there are not organized in this pass.

## Principles
1. **Keep active docs in root** - README, CHANGELOG, CONTRIBUTING, SECURITY
2. **Archive historical status** - Move to `docs/history/` with date prefixes
3. **Group related docs** - Status docs together, plans together
4. **Preserve context** - Keep file names clear, add README in organized directories

---

## 1. consensus-proof Repository

### Current State
- 23 markdown files in root
- 4 files in `docs/`
- Mix of active docs, historical status, and implementation summaries

### Organization Structure

```
consensus-proof/
├── README.md                    # KEEP (active)
├── CHANGELOG.md                 # KEEP (active)
├── CONTRIBUTING.md              # KEEP (active)
├── SECURITY.md                  # KEEP (active)
├── docs/
│   ├── VERIFICATION.md          # KEEP (existing)
│   ├── KLEE_SETUP.md            # KEEP (existing)
│   ├── REFERENCE_NODE_RPC_TESTING.md  # KEEP (existing)
│   ├── TEST_DATA_SOURCES.md     # KEEP (existing)
│   │
│   ├── history/                 # NEW: Historical implementation docs
│   │   ├── implementation/
│   │   │   ├── IMPLEMENTATION_COMPLETE.md
│   │   │   ├── INTEGRATION_IMPLEMENTATION_SUMMARY.md
│   │   │   ├── MISSING_INTEGRATIONS_COMPLETE.md
│   │   │   └── CORE_BLINDSPOTS_IMPLEMENTATION_COMPLETE.md
│   │   │
│   │   ├── testing/
│   │   │   ├── TESTING_GAP_RESOLUTION_STATUS.md
│   │   │   ├── TESTING_GAP_RESOLUTION_COMPLETE.md
│   │   │   ├── TESTING_GAP_RESOLUTION_FINAL.md
│   │   │   ├── TESTING_GAP_RESOLUTION_PHASE1_COMPLETE.md
│   │   │   ├── TESTING_GAP_RESOLUTION_PHASE2_COMPLETE.md
│   │   │   ├── TESTING_GAP_RESOLUTION_PHASE3_COMPLETE.md
│   │   │   ├── TESTING_GAP_RESOLUTION_PHASE4_COMPLETE.md
│   │   │   ├── TESTING_GAP_RESOLUTION_PHASE5_COMPLETE.md
│   │   │   └── TEST_BINARIES_FIXED.md
│   │   │
│   │   └── priority1/
│   │       ├── PRIORITY1_STATUS.md
│   │       ├── PRIORITY1_PROGRESS.md
│   │       ├── PRIORITY1_STATUS_UPDATE.md
│   │       └── PRIORITY1_COMPILATION_COMPLETE.md
│   │
│   ├── plans/                   # NEW: Planning documents
│   │   ├── PLAN_IMPLEMENTATION_STATUS.md
│   │   ├── PLAN_IMPLEMENTATION_FINAL.md
│   │   └── TEST_COVERAGE_PARITY_PLAN.md
│   │
│   └── fixes/                   # NEW: Bug fix documentation
│       └── SPAM_FILTER_FIX.md
│
└── fuzz/                        # KEEP (fuzzing infrastructure)
    └── ...
```

### Files to Move

**To `docs/history/implementation/`:**
- `IMPLEMENTATION_COMPLETE.md`
- `INTEGRATION_IMPLEMENTATION_SUMMARY.md`
- `MISSING_INTEGRATIONS_COMPLETE.md`
- `CORE_BLINDSPOTS_IMPLEMENTATION_COMPLETE.md`

**To `docs/history/testing/`:**
- `TESTING_GAP_RESOLUTION_STATUS.md`
- `TESTING_GAP_RESOLUTION_COMPLETE.md`
- `TESTING_GAP_RESOLUTION_FINAL.md`
- `TESTING_GAP_RESOLUTION_PHASE1_COMPLETE.md`
- `TESTING_GAP_RESOLUTION_PHASE2_COMPLETE.md`
- `TESTING_GAP_RESOLUTION_PHASE3_COMPLETE.md`
- `TESTING_GAP_RESOLUTION_PHASE4_COMPLETE.md`
- `TESTING_GAP_RESOLUTION_PHASE5_COMPLETE.md`
- `TEST_BINARIES_FIXED.md`

**To `docs/history/priority1/`:**
- `PRIORITY1_STATUS.md`
- `PRIORITY1_PROGRESS.md`
- `PRIORITY1_STATUS_UPDATE.md`
- `PRIORITY1_COMPILATION_COMPLETE.md`

**To `docs/plans/`:**
- `PLAN_IMPLEMENTATION_STATUS.md`
- `PLAN_IMPLEMENTATION_FINAL.md`
- `TEST_COVERAGE_PARITY_PLAN.md`

**To `docs/fixes/`:**
- `SPAM_FILTER_FIX.md`

---

## 2. reference-node Repository

### Current State
- 9 markdown files in root
- Multiple README and STATUS files

### Organization Structure

```
reference-node/
├── README.md                    # KEEP (active, main)
├── CHANGELOG.md                 # KEEP (active, main)
├── CONTRIBUTING.md              # KEEP (active)
├── SECURITY.md                  # KEEP (active)
├── docs/
│   ├── transport/
│   │   ├── README_TRANSPORT_ABSTRACTION.md
│   │   └── CHANGELOG_TRANSPORT.md
│   │
│   └── status/
│       ├── IMPLEMENTATION_STATUS.md
│       ├── IROH_API_INTEGRATION_STATUS.md
│       └── RPC_IMPLEMENTATION_STATUS.md
```

### Files to Move

**To `docs/transport/`:**
- `README_TRANSPORT_ABSTRACTION.md`
- `CHANGELOG_TRANSPORT.md`

**To `docs/status/`:**
- `IMPLEMENTATION_STATUS.md`
- `IROH_API_INTEGRATION_STATUS.md`
- `RPC_IMPLEMENTATION_STATUS.md`

---

## 3. Other Repositories

### developer-sdk
- **Issue**: Coverage reports in root (`coverage-final/`, `coverage-lib/`)
- **Action**: Add to `.gitignore` or move to `target/coverage/`
- **Keep**: Standard docs (README, CHANGELOG, CONTRIBUTING, SECURITY)

### protocol-engine
- **Status**: Clean, minimal root docs
- **Action**: None needed

### governance-app
- **Status**: Clean, minimal root docs
- **Action**: None needed

### commons
- **Status**: Clean, minimal root docs
- **Action**: None needed

---

## Implementation Steps

1. **Create directory structure** in each repo
2. **Move files** using `git mv` to preserve history
3. **Create README.md** in new directories explaining organization
4. **Update any references** to moved files (see Cross-References section)
5. **Commit changes** with clear organization messages

## Cross-References to Update

### consensus-proof

**Files that reference other docs:**
- `PLAN_IMPLEMENTATION_FINAL.md` references:
  - `IMPLEMENTATION_COMPLETE.md` → Update to `docs/history/implementation/IMPLEMENTATION_COMPLETE.md`
  - `SPAM_FILTER_FIX.md` → Update to `docs/fixes/SPAM_FILTER_FIX.md`

- `TESTING_GAP_RESOLUTION_STATUS.md` references:
  - Phase files → Update to `docs/history/testing/` paths

- `TESTING_GAP_RESOLUTION_COMPLETE.md` references:
  - Phase files → Update to `docs/history/testing/` paths

- `TESTING_GAP_RESOLUTION_FINAL.md` references:
  - Phase files → Update to `docs/history/testing/` paths

**Action**: After moving files, search and replace relative paths in these files.

## Notes

- Use `git mv` to preserve file history
- Some files reference other docs - update paths after moving
- Historical docs can be archived but kept for reference
- Active documentation (README, CHANGELOG) stays in root
- Consider adding symlinks or README redirects if external references exist

