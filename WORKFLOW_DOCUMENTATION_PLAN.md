# Workflow Documentation Improvements Plan

## Documentation Structure

**Key Understanding**: 
- **blvm-docs** = MAIN comprehensive documentation repository
- **Other repos** = Minimal docs as needed (not comprehensive)

## Current State

### What Exists in blvm-docs
- ✅ `development/testing.md` - Testing infrastructure
- ✅ `development/fuzzing.md` - Fuzzing infrastructure
- ✅ `development/benchmarking.md` - Benchmarking
- ✅ `development/differential-testing.md` - Differential testing
- ✅ `development/property-based-testing.md` - Property-based testing
- ✅ `development/snapshot-testing.md` - Snapshot testing
- ✅ `appendices/contributing-docs.md` - How to contribute to docs (minimal)

### What Exists in Other Repos (Should Be Consolidated)
- 📄 `blvm/docs/workflows/WORKFLOW_METHODOLOGY.md` (79 lines) - Technical org-wide workflow
- 📄 `blvm/docs/RELEASE_PROCESS.md` (337 lines) - Detailed release process
- 📄 `.github/CONTRIBUTING.md` (139 lines) - Basic contributing guide
- 📄 Individual repo `CONTRIBUTING.md` files - Scattered repo-specific guidelines
- 📄 `SYSTEM_OVERVIEW.md` - Governance tiers information

### What's Missing in blvm-docs (Main Docs)
- ❌ **Developer workflow guide** - Complete contribution process
- ❌ **PR process documentation** - Governance tiers, review process
- ❌ **CI/CD workflow explanation** - What happens when you push code
- ❌ **Release workflow** - User-facing explanation of releases

## Meaningful Improvements

### 1. Developer Workflow Guide ⭐ **HIGH PRIORITY**

**Location**: `blvm-docs/src/development/contributing.md`

**Content** (consolidate from):
- `.github/CONTRIBUTING.md` - Basic contribution steps
- Individual repo `CONTRIBUTING.md` files - Repo-specific guidelines
- `SYSTEM_OVERVIEW.md` - Governance tier context

**Should Include**:
- Complete developer workflow from fork to merge
- Governance tier classification (what tier is my PR?)
- Review requirements by tier
- Testing requirements
- Code style and standards
- Commit message format
- PR checklist

**Why Meaningful**: Developers need clear guidance on how to contribute. Currently scattered across multiple files. **blvm-docs should be the single source of truth.**

### 2. CI/CD Workflow Documentation ⭐ **HIGH PRIORITY**

**Location**: `blvm-docs/src/development/ci-cd-workflows.md`

**Content** (extract from):
- `blvm/docs/workflows/WORKFLOW_METHODOLOGY.md` - Technical workflow details
- Actual workflow files in `.github/workflows/` - What actually runs

**Should Include**:
- What happens when you push code
- What CI runs on each repository
- How to interpret CI results
- How to debug CI failures
- Self-hosted runner information
- Workflow dependencies and ordering

**Why Meaningful**: Developers need to understand what CI does and how to fix failures. **Currently only in blvm/docs, should be in main docs.**

### 3. PR Review Process Guide ⭐ **MEDIUM PRIORITY**

**Location**: `blvm-docs/src/development/pr-process.md`

**Content** (extract from):
- `SYSTEM_OVERVIEW.md` - Governance tiers and PR process
- Governance documentation in `blvm-docs/src/governance/` - Tier details

**Should Include**:
- Governance tier system explained
- Review period durations
- Signature requirements
- Economic node veto (for Tier 3+)
- Emergency procedures
- How to get your PR reviewed

**Why Meaningful**: Clear process reduces confusion and speeds up contributions. **Should be in main docs, not just SYSTEM_OVERVIEW.md.**

### 4. Release Process (User-Facing) ⭐ **LOW PRIORITY**

**Location**: `blvm-docs/src/development/release-process.md`

**Content** (extract from):
- `blvm/docs/RELEASE_PROCESS.md` - Detailed technical release process

**Should Include**:
- How releases are created
- Release variants (base vs experimental)
- Version numbering
- How to get notified of releases
- Release verification

**Why Meaningful**: Users need to understand releases. **Currently only in blvm/docs, should be in main docs.**

## Recommended Implementation Order

### Phase 1: Critical Developer Workflows
1. **Developer Workflow Guide** (`development/contributing.md`) - Complete end-to-end contribution process
2. **CI/CD Workflow Documentation** (`development/ci-cd-workflows.md`) - What happens in CI

### Phase 2: Process Documentation
3. **PR Review Process** (`development/pr-process.md`) - Governance tiers and review requirements

### Phase 3: User Information
4. **Release Process** (`development/release-process.md`) - User-facing release information

**Note**: Testing workflow is already covered by `development/testing.md` and related files.

## Content Sources (Consolidate Into blvm-docs)

**Extract from other repos**:
- `blvm/docs/workflows/WORKFLOW_METHODOLOGY.md` (79 lines) → `development/ci-cd-workflows.md`
- `blvm/docs/RELEASE_PROCESS.md` (337 lines) → `development/release-process.md`
- `.github/CONTRIBUTING.md` (139 lines) → `development/contributing.md`
- `SYSTEM_OVERVIEW.md` (governance tiers) → `development/pr-process.md`
- Individual repo `CONTRIBUTING.md` files → `development/contributing.md` (repo-specific sections)

**Create new**:
- Unified developer workflow (consolidate scattered info)
- CI/CD explanation (extract from technical docs, make user-friendly)
- PR process guide (extract from SYSTEM_OVERVIEW, expand)

## Estimated Impact

**High Priority Items**:
- Developer workflow guide: **HIGH** - Will significantly improve contributor experience, consolidates scattered info
- CI/CD documentation: **HIGH** - Will reduce support burden and confusion, currently only in blvm/docs

**Medium Priority Items**:
- PR process: **MEDIUM** - Helps but governance docs partially cover this, should be in main docs

**Low Priority Items**:
- Release process: **LOW** - Nice to have but less critical, currently only in blvm/docs

## Validation ✅

**Structure Understanding**:
- ✅ blvm-docs = MAIN comprehensive documentation
- ✅ Other repos = Minimal docs as needed
- ✅ Plan consolidates scattered docs into blvm-docs
- ✅ Plan adds missing workflow documentation to main docs

**Files to Create**:
- ✅ `blvm-docs/src/development/contributing.md` - NEW
- ✅ `blvm-docs/src/development/ci-cd-workflows.md` - NEW
- ✅ `blvm-docs/src/development/pr-process.md` - NEW
- ✅ `blvm-docs/src/development/release-process.md` - NEW

**Files to Update**:
- ✅ `blvm-docs/src/SUMMARY.md` - Add new docs to navigation

**Plan Status**: ✅ **VALIDATED** - Correctly identifies blvm-docs as main docs and consolidates scattered content

