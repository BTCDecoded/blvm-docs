# Documentation Release System

## Overview

The bllvm-docs release system provides versioned documentation snapshots, allowing users to access documentation for specific versions of the BLLVM system.

## Current System Analysis

### What We Have ✅

1. **Version File**: `VERSION` contains current version (e.g., `1.0.0`)
2. **Version Display**: Version shown in `INDEX.md` and `README.md`
3. **Archive System**: `archive-version.sh` archives docs to `archive/versions/vX.Y/`
4. **Auto-Update**: GitHub Pages workflow updates version in docs on deploy
5. **Archive Workflow**: Manual GitHub Actions workflow for archiving

### What's Missing ❌

1. **Release Tags**: No Git tags for documentation versions
2. **Release Notes**: No changelog or release notes
3. **GitHub Releases**: No GitHub releases created
4. **Automated Release**: No automated release process
5. **Version Bumping**: No automated version increment
6. **Release Artifacts**: No packaged releases

## Proposed Release System

### Release Types

1. **Major Releases** (X.0.0): Significant documentation restructure, new major BLLVM version
2. **Minor Releases** (X.Y.0): New documentation sections, major updates
3. **Patch Releases** (X.Y.Z): Bug fixes, corrections, minor updates

### Release Process

#### 1. Pre-Release Checklist

- [ ] All documentation is up to date
- [ ] Version extracted from source code is current
- [ ] All links are valid
- [ ] Documentation follows principles (timeless, imperative, etc.)
- [ ] No "coming soon" or placeholder content

#### 2. Release Creation

**Manual Process:**
```bash
# 1. Update VERSION file
echo "1.1.0" > VERSION

# 2. Update version in docs
python3 tools/update-version-in-docs.py

# 3. Archive previous major version (if needed)
./tools/archive-version.sh

# 4. Commit changes
git add VERSION INDEX.md README.md archive/
git commit -m "Release documentation v1.1.0"

# 5. Create tag
git tag -a v1.1.0 -m "Documentation release v1.1.0"

# 6. Push
git push origin main
git push origin v1.1.0
```

**Automated Process (GitHub Actions):**
- Trigger: Manual workflow dispatch
- Inputs: Version number, release notes
- Actions:
  1. Update VERSION file
  2. Update version in docs
  3. Archive if major version change
  4. Create commit
  5. Create Git tag
  6. Create GitHub release
  7. Push changes

#### 3. Post-Release

- GitHub release created with:
  - Release notes
  - Link to archived version (if major)
  - Link to current documentation
- Documentation deployed to GitHub Pages
- Archive available at `archive/versions/vX.Y/`

### Release Artifacts

1. **Git Tag**: `v1.0.0`, `v1.1.0`, etc.
2. **GitHub Release**: With release notes
3. **Archive**: `archive/versions/v1.0/` (for major versions)
4. **Documentation Site**: Current version at root, archived at `/archive/versions/vX.Y/`

### Version Bumping Strategy

**Major Version (X.0.0):**
- New major BLLVM release
- Significant documentation restructure
- Breaking changes in documentation structure
- **Action**: Archive previous major version

**Minor Version (X.Y.0):**
- New documentation sections
- Major content additions
- New features documented
- **Action**: No archive needed

**Patch Version (X.Y.Z):**
- Bug fixes
- Corrections
- Minor updates
- Link fixes
- **Action**: No archive needed

## Integration with Existing System

### Archive System

The archive system (`archive-version.sh`) works perfectly for major version releases:
- Archives complete documentation snapshot
- Preserves exact state at that version
- Accessible via `archive/versions/vX.Y/`

### Version Display

Version is automatically updated in:
- `INDEX.md` - Main entry point
- `README.md` - Repository README
- Updated on every GitHub Pages deployment

### GitHub Pages

Current system:
- Root directory = latest version
- `archive/versions/vX.Y/` = archived versions

Proposed enhancement:
- Add version selector to INDEX.md
- Link to archived versions
- Show version history

## Release Workflow

### Automated Release Workflow

```yaml
name: Create Documentation Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version (e.g., 1.1.0)'
        required: true
      release_type:
        description: 'Release type'
        type: choice
        options: [major, minor, patch]
        required: true
      release_notes:
        description: 'Release notes'
        required: false

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Update Version
        run: |
          echo "${{ github.event.inputs.version }}" > VERSION
          python3 tools/update-version-in-docs.py
      
      - name: Archive if Major
        if: github.event.inputs.release_type == 'major'
        run: |
          ./tools/archive-version.sh || echo "Archive may exist"
      
      - name: Create Release
        uses: actions/create-release@v1
        with:
          tag_name: v${{ github.event.inputs.version }}
          release_name: Documentation v${{ github.event.inputs.version }}
          body: ${{ github.event.inputs.release_notes }}
          draft: false
          prerelease: false
      
      - name: Commit and Tag
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add VERSION INDEX.md README.md archive/
          git commit -m "Release documentation v${{ github.event.inputs.version }}" || echo "No changes"
          git tag -a v${{ github.event.inputs.version }} -m "Documentation release v${{ github.event.inputs.version }}"
          git push origin main
          git push origin v${{ github.event.inputs.version }}
```

## Release Notes Template

```markdown
# Documentation Release v1.1.0

## What's New

- Added new section: [Section Name]
- Updated: [What was updated]
- Fixed: [What was fixed]

## Changes

### Added
- New documentation for [feature]

### Updated
- Updated [section] with [changes]

### Fixed
- Fixed broken links in [section]
- Corrected [error] in [section]

## Archive

Previous major version archived at: `archive/versions/v1.0/`

## Links

- [Current Documentation](https://btcdecoded.github.io/bllvm-docs/)
- [Archived v1.0](https://btcdecoded.github.io/bllvm-docs/archive/versions/v1.0/)
```

## Validation

### Current System ✅

1. **Version Management**: ✅ VERSION file exists
2. **Version Display**: ✅ Shown in INDEX.md and README.md
3. **Archive System**: ✅ archive-version.sh works
4. **Auto-Update**: ✅ GitHub Pages updates version
5. **Archive Workflow**: ✅ Manual archive workflow exists

### Proposed Enhancements 🔄

1. **Git Tags**: ⚠️ Not automated (manual only)
2. **GitHub Releases**: ❌ Not created
3. **Release Notes**: ❌ No template or process
4. **Automated Release**: ❌ No automated workflow
5. **Version Selector**: ❌ No UI for switching versions

### Recommendations

**Priority 1 (Essential):**
1. Create automated release workflow
2. Add Git tag creation to release process
3. Create GitHub releases with release notes

**Priority 2 (Important):**
4. Add version selector to INDEX.md
5. Create release notes template
6. Document release process

**Priority 3 (Nice to Have):**
7. Automated version bumping (semantic versioning)
8. Release changelog generation
9. Release artifact packaging

## Next Steps

1. Create automated release workflow
2. Add release notes template
3. Document release process in README
4. Test release process
5. Create first release

