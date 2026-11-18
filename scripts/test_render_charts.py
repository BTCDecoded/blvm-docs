#!/usr/bin/env python3
"""Checks for scripts/render-charts.py. Uses the governance YAML in this checkout."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import yaml

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "render_charts", ROOT / "scripts" / "render-charts.py"
)
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)


class RenderChartsTest(unittest.TestCase):
    def test_axis_uses_whole_ticks(self):
        self.assertEqual(rc.axis_ceiling(7), 7)
        self.assertEqual(rc.axis_ceiling(180), 200)
        self.assertEqual(rc.axis_ceiling(365), 400)
        self.assertEqual(rc.axis_ticks(200), [0, 50, 100, 150, 200])

    def test_binomial_known_values(self):
        self.assertEqual(rc.binom_at_least(7, 6, 0), 0)
        self.assertEqual(rc.binom_at_least(7, 6, 1), 1)
        self.assertAlmostEqual(rc.binom_at_least(1, 1, 0.5), 0.5)
        self.assertAlmostEqual(rc.binom_at_least(7, 6, 0.5), 8 / 128)

    def test_layers_follow_yaml(self):
        layers = rc.load_layers()
        raw = yaml.safe_load(
            (ROOT / "modules/governance/config/repository-layers.yml").read_text(encoding="utf-8")
        )["layers"]
        self.assertEqual(len(layers), 5)
        for row, key in zip(layers, rc.LAYER_KEYS):
            src = raw[key]
            self.assertEqual(row["required"], src["signatures"]["required"])
            self.assertEqual(row["total"], src["signatures"]["total"])
            self.assertEqual(row["review"], src["review_period_days"])

    def test_tiers_are_the_five_action_tiers(self):
        tiers = rc.load_tiers()
        self.assertEqual([row["key"] for row in tiers], [key for key, _ in rc.TIER_KEYS])
        self.assertNotIn("security_critical", [row["key"] for row in tiers])

    def test_identical_quorums_share_a_curve(self):
        groups = rc.quorum_groups(rc.load_layers())
        merged = [g for g in groups if g["key"] == (6, 7)]
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["labels"], ["L1 spec", "L2 consensus"])

    def test_policy_charts_contain_yaml_numbers(self):
        layers = rc.load_layers()
        rendered = rc.outputs()
        layer_svg = rendered[ROOT / "src/images/charts/layer-thresholds.svg"]
        for row in layers:
            self.assertIn(f">{row['review']}<", layer_svg)
            if row["consensus_review"] is not None:
                self.assertIn(f">{row['consensus_review']}<", layer_svg)
        self.assertIn("Policy windows", layer_svg)
        tier_svg = rendered[ROOT / "src/images/charts/tier-review-days.svg"]
        for row in rc.load_tiers():
            self.assertIn(f">{row['days']}<", tier_svg)
        self.assertNotIn("Bitcoin Core", tier_svg)
        quorum = rendered[ROOT / "src/images/charts/quorum-capture.svg"]
        for group in rc.quorum_groups(layers):
            self.assertIn(group["name"], quorum)
        self.assertIn("not a measured attacker rate", quorum)

    def test_flows_keep_the_previous_labels(self):
        rendered = rc.outputs()
        spec = rendered[ROOT / "charts/fragments/spec-maintenance.md"]
        self.assertIn("AI extraction", spec)
        self.assertIn("Orange Paper updated", spec)
        self.assertIn("formal verification runs", spec)
        anchors = rendered[ROOT / "charts/fragments/verification-anchors.md"]
        self.assertIn("3-of-5 merge multisig", anchors)
        self.assertIn("webhook gate", anchors)
        self.assertIn("court-grade record", anchors)
        block = rendered[ROOT / "charts/fragments/block-path.md"]
        self.assertIn("Governance logging", block)
        self.assertIn("Module execution", block)
        gates = rendered[ROOT / "src/images/charts/release-gates.svg"]
        self.assertIn("No series is published.", gates)
        self.assertNotIn(">60<", gates)

    def test_audit_cells_match_the_governance_wording(self):
        svg = rc.outputs()[ROOT / "src/images/charts/audit-completeness.svg"]
        self.assertEqual(svg.count(">designed<"), 3)
        self.assertEqual(svg.count(">absent<"), 1)
        self.assertEqual(svg.count(">complete<"), 0)
        self.assertIn("Live enforcement", svg)
        self.assertIn("Bitcoin Commons", svg)

    def test_carried_pngs_match_the_pinned_bytes(self):
        import hashlib

        carried = [c for c in rc.load_catalog() if c.get("sha256")]
        self.assertEqual(len(carried), 4)
        for chart in carried:
            digest = hashlib.sha256((ROOT / chart["source"]).read_bytes()).hexdigest()
            self.assertEqual(digest, chart["sha256"], chart["id"])

    def test_coverage_figures_are_drawn_from_series_files(self):
        rendered = rc.outputs()
        attrs = rendered[ROOT / "src/images/charts/consensus-coverage.svg"]
        for value in (18, 40, 13, 2, 16):
            self.assertIn(f">{value}<", attrs)
        self.assertIn("Total 281", attrs)
        self.assertIn("Not the 13 body proofs", attrs)
        self.assertNotIn(
            ROOT / "src/images/charts/spec-drift-vs-test-coverage.svg", rendered
        )

    def test_assurance_scoreboard_keeps_each_list(self):
        svg = rc.scoreboard_chart(
            {
                "id": "assurance-counts",
                "title": "What locks the implementation",
                "measure": "Headline counts. Each figure has its own list",
            }
        )
        for value in ("281", "13", "93/224", "34/34", "2,353", "187", "63", "16", "1"):
            self.assertIn(f">{value}<", svg)
        self.assertIn("Spec-locked functions", svg)
        self.assertIn("Also checked in Rust", svg)

    def test_sentence_coverage_keeps_the_one_sentence_overlap(self):
        svg = rc.hbar_chart(
            {
                "id": "sentence-coverage",
                "title": "Orange Paper sentences",
                "measure": "Each of the 275 sentences once. Lean and Rust is theorem 6.1.2",
                "unit": "sentences",
            }
        )
        for label, count in (
            ("Lean and Rust", 1),
            ("Lean only", 15),
            ("Disputed", 1),
            ("Model unwritten", 137),
            ("Parse failed", 119),
        ):
            self.assertIn(label, svg)
            self.assertIn(f">{count}<", svg)
        self.assertNotIn("<polygon", svg)

    def test_consensus_test_counts_sum_to_the_functions(self):
        svg = rc.hbar_chart(
            {
                "id": "consensus-tests",
                "title": "Consensus test functions",
                "measure": "#[test] and #[tokio::test] in blvm-consensus, one bar per area",
                "unit": "tests",
            }
        )
        shown = [644, 420, 301, 184, 171, 147, 115, 104, 92, 63, 62, 50]
        self.assertEqual(sum(shown), 2353)
        for count in shown:
            self.assertIn(f">{count}<", svg)
        self.assertIn("Script, witness, sighash", svg)
        self.assertIn("2,353 functions", svg)

    def test_missing_series_stays_empty(self):
        svg = rc.series_chart(
            {
                "id": "not-a-published-series",
                "title": "Unused",
                "measure": "Nothing published",
                "unit": "days",
            }
        )
        self.assertIn("No series is published.", svg)
        self.assertNotIn("<polyline", svg)

    def test_measured_series_draws_its_values(self):
        path = rc.series_path("not-a-published-series")
        self.assertFalse(path.exists())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(
                {
                    "status": "measured",
                    "measured_at": "2026-11-14",
                    "source": "fixture",
                    "unit": "developer-weeks",
                    "categories": ["consensus"],
                    "series": [{"name": "weeks", "values": [3]}],
                }
            ),
            encoding="utf-8",
        )
        try:
            svg = rc.series_chart(
                {
                    "id": "not-a-published-series",
                    "title": "Unused",
                    "measure": "Nothing published",
                    "unit": "days",
                }
            )
            self.assertIn(">3<", svg)
            self.assertIn("2026-11-14", svg)
            self.assertIn("fixture", svg)
        finally:
            path.unlink()

    def test_measured_series_rejects_a_short_row(self):
        path = rc.series_path("pr-review-time")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "status: measured\nmeasured_at: '2026-11-14'\nsource: fixture\n"
            "unit: days\ncategories: [a, b]\nseries:\n  - name: median\n    values: [1]\n",
            encoding="utf-8",
        )
        try:
            with self.assertRaises(SystemExit):
                rc.load_series("pr-review-time")
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
