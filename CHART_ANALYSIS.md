# Chart Analysis and Documentation Placement

## Summary

This document analyzes charts/images from the btcdecoded-book manuscript and identifies appropriate placements in the documentation.

## Chart Inventory

### Charts Referenced in Manuscript

The manuscript references charts from multiple directories:
- `images2/` - Governance and process charts
- `images3/` - Economic and adoption charts  
- `images4/` - Architecture and implementation charts
- `images5/` - Process and workflow charts
- `images6/` - System architecture and verification charts
- `images7/` - Stack and principles charts
- `images/` - Architecture comparison charts

### Charts Available in commons-website

Many charts are already available in `commons-website/assets/images/` and can be referenced from the documentation.

## Chart Mapping to Documentation Sections

### Architecture Section

**Recommended Charts:**
1. **stack.png** - BLLVM Stack Architecture
   - **Placement**: `src/architecture/system-overview.md`
   - **Context**: Shows the complete 6-tier architecture
   - **Source**: `images7/stack.png` or `commons-website/assets/images/stack.png`

2. **architecture-trans.png** - Complete Bitcoin Commons Architecture
   - **Placement**: `src/architecture/system-overview.md`
   - **Context**: Shows seven-repository architecture
   - **Source**: `images/architecture-trans.png`

3. **tier-architecture.png** - Tiered Architecture
   - **Placement**: `src/architecture/component-relationships.md`
   - **Context**: Shows tier breakdown (Tier 1-4)
   - **Source**: `images6/tier-architecture.png` or `commons-website/assets/images/tier-architecture.png`

4. **how-the-stack-works-in-practice.png** - Data Flow
   - **Placement**: `src/architecture/component-relationships.md`
   - **Context**: End-to-end data flow through components
   - **Source**: `images6/how-the-stack-works-in-practice.png` or `commons-website/assets/images/how-the-stack-works-in-practice.png`

5. **architecture-comparison-trans.png** - Core vs Commons
   - **Placement**: `src/architecture/design-philosophy.md`
   - **Context**: Architectural comparison
   - **Source**: `images/architecture-comparison-trans.png`

### Consensus Layer Section

**Recommended Charts:**
1. **Consensus-Coverage-Comparison.png** - Coverage Comparison
   - **Placement**: `src/consensus/formal-verification.md`
   - **Context**: Shows formal verification coverage vs testing
   - **Source**: `images7/Consensus-Coverage-Comparison.png` or `commons-website/assets/images/Consensus-Coverage-Comparison.png`

2. **spec-drift-vs-test-coverage.png** - Spec Drift Analysis
   - **Placement**: `src/consensus/mathematical-correctness.md`
   - **Context**: Shows how test coverage reduces spec drift
   - **Source**: `images2/spec-drift-vs-test-coverage.png` or `commons-website/assets/images/spec-drift-vs-test-coverage.png`

3. **spec-maintenance-workflow.png** - Spec Maintenance
   - **Placement**: `src/consensus/architecture.md`
   - **Context**: Shows spec maintenance workflow
   - **Source**: `images7/spec-maintenance-workflow.png` or `commons-website/assets/images/spec-maintenance-workflow.png`

4. **proof-maintenance-cost.png** - Proof Maintenance Cost
   - **Placement**: `src/consensus/formal-verification.md`
   - **Context**: Shows proof maintenance cost by area
   - **Source**: `images5/proof-maintenance-cost.png` or `commons-website/assets/images/proof-maintenance-cost.png`

### Governance Section

**Recommended Charts:**
1. **governance-signature-thresholds.png** - Signature Thresholds
   - **Placement**: `src/governance/multisig-configuration.md`
   - **Context**: Shows layer-based signature thresholds
   - **Source**: `images4/governance-signature-thresholds.png` or `commons-website/assets/images/governance-signature-thresholds.png`

2. **three-layer-verification-arch.png** - Three-Layer Verification
   - **Placement**: `src/governance/audit-trails.md`
   - **Context**: Shows GitHub, Nostr, OpenTimestamps layers
   - **Source**: `images6/three-layer-verification-arch.png` or `commons-website/assets/images/three-layer-verification-arch.png`

3. **three-layer-verification-arch0.png** - Verification Overview
   - **Placement**: `src/governance/audit-trails.md`
   - **Context**: Overview of verification approach
   - **Source**: `images6/three-layer-verification-arch0.png` or `commons-website/assets/images/three-layer-verification-arch0.png`

4. **attack-path-interception-map.png** - Attack Path Interception
   - **Placement**: `src/governance/overview.md`
   - **Context**: Risk interception points
   - **Source**: `images2/attack-path-interception-map.png` or `commons-website/assets/images/attack-path-interception-map.png`

5. **audit-trail-completeness.png** - Audit Trail Completeness
   - **Placement**: `src/governance/audit-trails.md`
   - **Context**: Completeness across governance layers
   - **Source**: `images2/audit-trail-completeness.png` or `commons-website/assets/images/audit-trail-completeness.png`

6. **release-pipeline-gate-strength.png** - Release Pipeline Gates
   - **Placement**: `src/governance/keyholder-procedures.md`
   - **Context**: Gate strength across release pipeline
   - **Source**: `images2/release-pipeline-gate-strength.png` or `commons-website/assets/images/release-pipeline-gate-strength.png`

7. **pr-review-time-distribution.png** - PR Review Time
   - **Placement**: `src/governance/governance-model.md`
   - **Context**: Shows why throughput stalls
   - **Source**: `images6/pr-review-time-distribution.png` or `commons-website/assets/images/pr-review-time-distribution.png`

8. **governance-process-latency.png** - Process Latency
   - **Placement**: `src/governance/governance-model.md`
   - **Context**: Governance process timing
   - **Source**: `commons-website/assets/images/governance-process-latency.png`

9. **multisig-threshold-sensitivity.png** - Multisig Sensitivity
   - **Placement**: `src/governance/multisig-configuration.md`
   - **Context**: Threshold sensitivity analysis
   - **Source**: `commons-website/assets/images/multisig-threshold-sensitivity.png`

### Reference Section

**Recommended Charts:**
1. **principles_matrix_complete.png** - Principles Matrix
   - **Placement**: `src/reference/orange-paper.md` or new `src/reference/principles.md`
   - **Context**: Bitcoin Commons principles
   - **Source**: `images7/principles_matrix_complete.png` or `commons-website/assets/images/principles_matrix_complete.png`

## Implementation Plan

### Step 1: Copy Charts to Documentation

Since charts are in `commons-website/assets/images/`, we can:
1. Reference them directly from commons-website (if same domain)
2. Copy to `bllvm-docs/src/images/` for self-contained docs
3. Use relative paths from submodules

**Recommendation**: Copy charts to `bllvm-docs/src/images/` for self-contained documentation.

### Step 2: Add Chart References

Update documentation files to include charts using mdBook image syntax:

```markdown
![Chart Title](../images/chart-name.png)
*Figure: Chart description and context.*
```

### Step 3: Verify Chart Availability

Check that all referenced charts exist in commons-website or need to be copied from btcdecoded-book.

## Chart Validation Status

### Charts in Manuscript ✅
- All charts referenced in manuscript are documented above

### Charts in commons-website ✅
- Most charts are available in `commons-website/assets/images/`

### Charts Missing ⚠️
- Some charts may only exist in btcdecoded-book directories
- Need to verify and copy if needed

## Next Steps

1. Create `bllvm-docs/src/images/` directory
2. Copy relevant charts from commons-website or btcdecoded-book
3. Update documentation files with chart references
4. Test that charts render correctly in mdBook

