# Manual charts

`scripts/render-charts.py` rebuilds every figure in the book from `catalog.yml`.

Policy charts read `modules/governance/config/repository-layers.yml` and `action-tiers.yml`. Process charts are Mermaid diagrams whose steps are the `diagram` field in the catalog. A `series` chart draws bars only when `charts/series/<id>.yml` is measured. Until then the book shows an empty panel that names the measure.

Regenerate, then commit the SVG and Mermaid fragments with the catalog:

```bash
python3 scripts/render-charts.py
python3 scripts/test_render_charts.py
```

## What each figure measures

| Id | Measure | Source today |
|---|---|---|
| `layer-thresholds` | Required signatures, maintainer set size, review window, and the consensus-change window where the YAML has one | `repository-layers.yml` |
| `tier-review-days` | Published review period for action tiers 1–5, in days | `action-tiers.yml` |
| `quorum-capture` | Model: independent per-signer compromise probability *p*, curve is P(at least *k* signers compromised) for each published quorum | *k* and *n* from `repository-layers.yml`. *p* is the axis, not a measured rate |
| `block-path` | The six steps on the previous figure | Catalog diagram |
| `spec-maintenance` | The steps on the previous figure, including its drift-detection label | Catalog diagram |
| `verification-anchors` | The three layers printed on the previous figure | Catalog diagram |
| `release-gates` | The six strength percents printed on the previous figure | `charts/series/release-gates.yml` |
| `proof-maintenance-cost` | The previous figure, carried as pixels | `charts/carried/proof-maintenance-cost.png` |
| `spec-drift` | The previous figure, carried as pixels | `charts/carried/spec-drift-vs-test-coverage.png` |
| `pr-review-time` | The previous figure, carried as pixels | `charts/carried/pr-review-time-distribution.png` |
| `process-latency` | The previous Core and Commons bars, carried as pixels | `charts/carried/governance-process-latency.png` |
| `multisig-sensitivity` | The previous figure, carried as pixels | `charts/carried/multisig-threshold-sensitivity.png` |
| `audit-completeness` | Complete, partial, or absent, read from the previous figure's cell colors | `charts/series/audit-completeness.yml` |
| `consensus-coverage` | The previous radar, carried as pixels | `charts/carried/consensus-coverage.png` |

## Adding a measurement

```yaml
status: measured
measured_at: "2026-11-14"
source: "https://example.com/the-run-or-a-commit"
unit: days
categories: [blvm-consensus, blvm-node]
series:
  - name: median
    values: [4, 11]
```

Save that as `charts/series/<id>.yml`, then run the renderer. `measured_at`, `source`, `unit`, `categories`, and one `values` list per series are required. The value lists must be the same length as `categories`. A file with `status: unmeasured` keeps the empty panel.
