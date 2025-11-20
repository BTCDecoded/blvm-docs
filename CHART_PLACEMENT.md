# Chart Placement Plan

## Chart Validation Summary

### Charts in Manuscript AND commons-website (✅ Available)
These charts are referenced in the manuscript and available in commons-website:

1. **stack.png** - BLLVM Stack Architecture
2. **tier-architecture.png** - Tiered Architecture
3. **how-the-stack-works-in-practice.png** - Data Flow
4. **Consensus-Coverage-Comparison.png** - Coverage Comparison
5. **spec-drift-vs-test-coverage.png** - Spec Drift Analysis
6. **spec-maintenance-workflow.png** - Spec Maintenance
7. **proof-maintenance-cost.png** - Proof Maintenance Cost
8. **governance-signature-thresholds.png** - Signature Thresholds
9. **three-layer-verification-arch.png** - Three-Layer Verification
10. **three-layer-verification-arch0.png** - Verification Overview
11. **attack-path-interception-map.png** - Attack Path Interception
12. **audit-trail-completeness.png** - Audit Trail Completeness
13. **release-pipeline-gate-strength.png** - Release Pipeline Gates
14. **pr-review-time-distribution.png** - PR Review Time
15. **governance-process-latency.png** - Process Latency
16. **multisig-threshold-sensitivity.png** - Multisig Sensitivity
17. **principles_matrix_complete.png** - Principles Matrix
18. **upgrade-safety-checklist.png** - Upgrade Safety
19. **keyholder-diversity-radar.png** - Keyholder Diversity
20. **decision-provenance-completeness.png** - Decision Provenance
21. **economic-veto-threshold.png** - Economic Veto
22. **development-trajectory.png** - Development Trajectory
23. **sustainability-ecosystem-health.png** - Sustainability
24. **module-quality-control-process.png** - Module Quality
25. **fragmentation-analysis.png** - Fragmentation Analysis
26. **economic-alignment.png** - Economic Alignment
27. **funding-trans.png** - Funding Model
28. **revenue-allocation-2.png** - Revenue Allocation
29. **miner-economic-sensitivity.png** - Miner Sensitivity
30. **sustainability-over-time-monolith-vs-modular.png** - Sustainability Over Time
31. **talent-bottleneck.png** - Talent Bottleneck
32. **the-economic-reality.png** - Economic Reality
33. **revenue-model-sensitivity-analysis.png** - Revenue Sensitivity
34. **secondary-chain-value-prop.png** - Secondary Chain Value
35. **community-health-radar.png** - Community Health
36. **governance-latency-stack.png** - Governance Latency Stack
37. **economic-scaling-trajectory.png** - Economic Scaling
38. **bitcoin-knots-surge.png** - Bitcoin Knots Surge
39. **centralized-vs-decentralized.png** - Centralized vs Decentralized

### Charts in Manuscript but NOT in commons-website (⚠️ Need to Copy)
These charts are referenced in manuscript but need to be copied from btcdecoded-book:

1. **architecture-trans.png** - Complete Architecture (in `images/`)
2. **architecture-comparison-trans.png** - Architecture Comparison (in `images/`)
3. **architecture-quality-TRANS.png** - Architecture Quality (in `images/`)
4. **attack-vectors-trans.png** - Attack Vectors (in `images/`)
5. **power_structure-trans.png** - Power Structure (in `images/`)
6. **Security-barriers-trans.png** - Security Barriers (in `images/`)
7. **governance-spof.png** - Governance SPOF (root level)
8. **governance-quality.png** - Governance Quality (root level)
9. **capture-resistance.png** - Capture Resistance (root level)
10. **capture-resistance-vs-attack-surface.png** - Capture vs Attack (root level)
11. **institutional-readiness.png** - Institutional Readiness (root level)
12. **institutional-risk.png** - Institutional Risk (root level)
13. **path-to-clarity.png** - Path to Clarity (root level)
14. **historical-timeline.png** - Historical Timeline (in `images6/`)
15. **bitcoin-power-centers.png** - Power Centers (in `images6/`)
16. **bus-factor-over-time.png** - Bus Factor (in `images6/`)
17. **knowledge-concentration-heatmap-developer-attrition.png** - Knowledge Concentration (in `images6/`)
18. **recovery-cost-vs-intervention-timing.png** - Recovery Cost (in `images6/`)
19. **governance-assymetry-snapshot.png** - Governance Asymmetry (in `images4/`)
20. **reviewer-capacity-vs-change-complexity.png** - Reviewer Capacity (in `images2/`)
21. **contribution-barrier-heights.png** - Contribution Barriers (in `images6/`)
22. **innovation-vs-maintenance-split.png** - Innovation vs Maintenance (in `images6/`)
23. **policy-vs-consensus.png** - Policy vs Consensus (in `images2/`)
24. **implementation-concentration.png** - Implementation Concentration (in `images4/`)
25. **spec-coverage.png** - Spec Coverage (in `images4/`)
26. **spec-drift-alerts.png** - Spec Drift Alerts (in `images5/`)
27. **maintainer-jurisdiction.png** - Maintainer Jurisdiction (in `images2/`)
28. **change-category-signature.png** - Change Category Signature (in `images2/`)

### Charts in commons-website but NOT in manuscript (✅ Available for Use)
These charts exist and can be used in documentation:

1. **bitcoin-commons-logo.png** - Logo
2. **principles_of_bitcoin_commons.png** - Principles (alternative version)

## Recommended Chart Placements

### Architecture Section

#### `src/architecture/system-overview.md`
- **stack.png** - BLLVM Stack Architecture (primary architecture diagram)
- **architecture-trans.png** - Complete Bitcoin Commons Architecture (if copied)
- **tier-architecture.png** - Tiered Architecture breakdown

#### `src/architecture/component-relationships.md`
- **how-the-stack-works-in-practice.png** - Data flow diagram
- **architecture-comparison-trans.png** - Core vs Commons comparison (if copied)

#### `src/architecture/design-philosophy.md`
- **centralized-vs-decentralized.png** - Governance comparison
- **governance-assymetry-snapshot.png** - Governance asymmetry (if copied)

### Consensus Layer Section

#### `src/consensus/formal-verification.md`
- **Consensus-Coverage-Comparison.png** - Coverage comparison
- **proof-maintenance-cost.png** - Proof maintenance cost
- **spec-drift-vs-test-coverage.png** - Spec drift analysis

#### `src/consensus/architecture.md`
- **spec-maintenance-workflow.png** - Spec maintenance workflow
- **spec-coverage.png** - Spec coverage (if copied)
- **spec-drift-alerts.png** - Spec drift alerts (if copied)

#### `src/consensus/mathematical-correctness.md`
- **Security-barriers-trans.png** - Security barriers (if copied)

### Governance Section

#### `src/governance/overview.md`
- **attack-path-interception-map.png** - Attack path interception
- **governance-spof.png** - Single point of failure (if copied)
- **bitcoin-power-centers.png** - Power centers (if copied)

#### `src/governance/governance-model.md`
- **governance-signature-thresholds.png** - Signature thresholds
- **governance-process-latency.png** - Process latency
- **governance-latency-stack.png** - Latency stack
- **pr-review-time-distribution.png** - PR review time
- **governance-assymetry-snapshot.png** - Asymmetry snapshot (if copied)

#### `src/governance/multisig-configuration.md`
- **multisig-threshold-sensitivity.png** - Threshold sensitivity
- **governance-signature-thresholds.png** - Signature thresholds (duplicate)

#### `src/governance/keyholder-procedures.md`
- **keyholder-diversity-radar.png** - Keyholder diversity
- **release-pipeline-gate-strength.png** - Release pipeline gates
- **maintainer-jurisdiction.png** - Maintainer jurisdiction (if copied)

#### `src/governance/audit-trails.md`
- **three-layer-verification-arch.png** - Three-layer verification
- **three-layer-verification-arch0.png** - Verification overview
- **audit-trail-completeness.png** - Audit trail completeness
- **decision-provenance-completeness.png** - Decision provenance

### Reference Section

#### `src/reference/orange-paper.md`
- **principles_matrix_complete.png** - Principles matrix
- **path-to-clarity.png** - Path to clarity (if copied)

#### New: `src/reference/governance-comparison.md`
- **capture-resistance.png** - Capture resistance (if copied)
- **capture-resistance-vs-attack-surface.png** - Capture vs attack (if copied)
- **governance-quality.png** - Governance quality (if copied)

### Getting Started Section

#### `src/getting-started/installation.md`
- **talent-bottleneck.png** - Why implementation diversity matters
- **contribution-barrier-heights.png** - Contribution barriers (if copied)

## Implementation Steps

1. **Create images directory**: `bllvm-docs/src/images/`
2. **Copy charts from commons-website**: Copy available charts
3. **Copy missing charts from btcdecoded-book**: Copy charts not in commons-website
4. **Update documentation files**: Add chart references using mdBook syntax
5. **Test rendering**: Verify charts display correctly

## Chart Reference Syntax

mdBook supports standard markdown image syntax:

```markdown
![Chart Title](../images/chart-name.png)
*Figure: Chart description and context.*
```

For better control, use HTML:

```html
<img src="../images/chart-name.png" alt="Chart Title" style="width: 100%;">
*Figure: Chart description and context.*
```

