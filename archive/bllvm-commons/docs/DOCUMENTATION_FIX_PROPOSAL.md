# Documentation Fix Proposal

**Date**: 2025-01-XX  
**Purpose**: Propose fixes for conflicting documentation about formal verification counts and system status

## Summary

This document proposes fixes for documentation that contains conflicting or outdated information about formal verification counts and system status. The goal is to ensure all documentation references the verified, authoritative source: `SYSTEM_STATUS.md`.

## Conflicting Documentation Issues

### 1. Formal Verification Count Conflicts

**Problem**: Multiple documents claim different counts of Kani proofs:
- `docs/FORMAL_VERIFICATION_STATUS.md`: Claims 13 proofs, 85% coverage
- `docs/FORMAL_VERIFICATION_STATUS_FINAL.md`: Claims 51 proofs, 99% coverage  
- `docs/FORMAL_VERIFICATION_99_PERCENT_ACHIEVED.md`: Claims 60 proofs, 99% coverage
- **Verified Actual**: 176 `kani::proof` calls in source code

**Proposed Fix**: Add deprecation notices to all conflicting documents pointing to `SYSTEM_STATUS.md`:

```markdown
> **⚠️ DEPRECATED**: This document contains outdated information. 
> For current verified formal verification status, see [SYSTEM_STATUS.md](../SYSTEM_STATUS.md). 
> Verified count: 176 kani::proof calls in source code.
```

**Files to Update**:
- `docs/FORMAL_VERIFICATION_STATUS.md` ✅ (already has deprecation notice)
- `docs/FORMAL_VERIFICATION_STATUS_FINAL.md`
- `docs/FORMAL_VERIFICATION_99_PERCENT_ACHIEVED.md`
- `docs/FORMAL_VERIFICATION_COMPREHENSIVE_SUMMARY.md`
- Any other documents claiming specific proof counts

### 2. Component Status Conflicts

**Problem**: Some documents claim components are "in progress" or "partial" when they are actually complete (Phase 1).

**Proposed Fix**: Add clarification notices:

```markdown
> **Note**: This document may contain outdated status information. 
> For current verified implementation status, see [SYSTEM_STATUS.md](../SYSTEM_STATUS.md).
> All components are implemented (Phase 1), but governance is not yet activated (Phase 2).
```

**Files to Review**:
- `GAP_ANALYSIS.md` (already references SYSTEM_STATUS.md)
- `INTEGRATION_SUMMARY.md`
- `PRE_RELEASE_REPORT.md`
- Any status documents not referencing SYSTEM_STATUS.md

### 3. Test Coverage Percentage Claims

**Problem**: Documents claim various coverage percentages without sources or verification.

**Proposed Fix**: Replace percentage claims with verified test file counts:

```markdown
> **Note**: Coverage percentages in this document are estimates. 
> For verified test counts, see [SYSTEM_STATUS.md](../SYSTEM_STATUS.md).
> Actual test file counts: bllvm-consensus (97 files), bllvm-node (29 files), etc.
```

## Implementation Plan

### Phase 1: Add Deprecation Notices (Immediate)

1. **Update conflicting formal verification documents**:
   - Add deprecation notice at top of each file
   - Point to SYSTEM_STATUS.md as authoritative source
   - Keep document for historical reference but mark as deprecated

2. **Update status documents**:
   - Add reference to SYSTEM_STATUS.md in introduction
   - Clarify Phase 1 vs Phase 2 distinction

### Phase 2: Archive Historical Documents (Future)

1. **Move to archive directory**:
   - Create `docs/archive/` directory
   - Move session summaries and milestone documents
   - Keep for historical reference but remove from active documentation

2. **Update documentation index**:
   - Mark archived documents clearly
   - Update links to point to SYSTEM_STATUS.md

### Phase 3: Establish Documentation Standards (Ongoing)

1. **Create documentation template**:
   - Include reference to SYSTEM_STATUS.md
   - Include deprecation notice template
   - Include Phase 1 vs Phase 2 clarification

2. **CI/CD checks**:
   - Add check to ensure new status documents reference SYSTEM_STATUS.md
   - Warn if documents claim specific proof counts without verification

## Specific File Updates

### Files Requiring Deprecation Notices

1. `docs/FORMAL_VERIFICATION_STATUS_FINAL.md`
   - Add: "⚠️ DEPRECATED: Claims 51 proofs. Verified: 176 proofs. See SYSTEM_STATUS.md"

2. `docs/FORMAL_VERIFICATION_99_PERCENT_ACHIEVED.md`
   - Add: "⚠️ DEPRECATED: Claims 60 proofs. Verified: 176 proofs. See SYSTEM_STATUS.md"

3. `docs/FORMAL_VERIFICATION_COMPREHENSIVE_SUMMARY.md`
   - Add: "⚠️ DEPRECATED: Contains outdated counts. See SYSTEM_STATUS.md"

### Files Requiring Status Clarification

1. `INTEGRATION_SUMMARY.md`
   - Add reference to SYSTEM_STATUS.md
   - Clarify Phase 1 vs Phase 2

2. `PRE_RELEASE_REPORT.md`
   - Add reference to SYSTEM_STATUS.md
   - Update any "in progress" claims to "Phase 1 complete"

## Verification

After implementing fixes:

1. **Search for conflicting claims**:
   ```bash
   grep -r "13 proofs\|51 proofs\|60 proofs" docs/
   grep -r "85%\|99%" docs/ | grep -i "verification\|proof"
   ```

2. **Verify all documents reference SYSTEM_STATUS.md**:
   ```bash
   find docs/ -name "*.md" -type f | xargs grep -L "SYSTEM_STATUS.md"
   ```

3. **Check for Phase 1 vs Phase 2 clarity**:
   ```bash
   grep -r "in progress\|partial\|incomplete" docs/ | grep -v "Phase 2"
   ```

## Benefits

1. **Single Source of Truth**: All documentation points to SYSTEM_STATUS.md
2. **Reduced Confusion**: Clear deprecation notices prevent outdated information
3. **Historical Preservation**: Documents kept for reference but marked deprecated
4. **Future Prevention**: Template and CI checks prevent new conflicts

## Timeline

- **Immediate**: Add deprecation notices to conflicting documents (1-2 hours)
- **Short-term**: Update status documents with references (2-4 hours)
- **Long-term**: Archive historical documents, establish standards (ongoing)

## Notes

- Keep deprecated documents for historical reference
- Don't delete documents, just mark as deprecated
- SYSTEM_STATUS.md remains the single source of truth
- All new documentation should reference SYSTEM_STATUS.md

