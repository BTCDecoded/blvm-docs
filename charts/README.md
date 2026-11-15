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
| `release-gates` | Gate strength | No series published |
| `proof-maintenance-cost` | Developer-weeks per quarter | No series published |
| `pr-review-time` | Monolith and modular review time | PNG pinned, not embedded. Draw from `charts/series/pr-review-time.yml` |
| `process-latency` | Review days by action tier | `tier-review-days`, from `action-tiers.yml`. The Core comparison PNG is pinned and not embedded |
| `multisig-sensitivity` | Quorum capture for the published signature counts | `quorum-capture`, from `repository-layers.yml`. The old sensitivity PNG is pinned and not embedded |
| `audit-completeness` | Commons audit controls: designed or absent | `charts/series/audit-completeness.yml` |
| `consensus-coverage` | Production spec_locked attributes by area. Total with witness fixtures is 281 | `charts/series/consensus-coverage.yml` |

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
