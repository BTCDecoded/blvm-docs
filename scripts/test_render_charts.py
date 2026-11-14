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
        for value in (60, 75, 80, 85, 90, 95):
            self.assertIn(f">{value}<", gates)
        self.assertIn("Phase 3 estimates", gates)

    def test_audit_cells_match_the_previous_figure(self):
        svg = rc.outputs()[ROOT / "src/images/charts/audit-completeness.svg"]
        self.assertEqual(svg.count(">complete<"), 8)
        self.assertEqual(svg.count(">partial<"), 18)
        self.assertEqual(svg.count(">absent<"), 4)
        self.assertIn("Merkle proofs", svg)
        self.assertIn("Bitcoin Commons", svg)

    def test_carried_pngs_match_the_previous_bytes(self):
        import hashlib
        import subprocess

        previous = {
            "pr-review-time-distribution.png": "src/images/pr-review-time-distribution.png",
            "proof-maintenance-cost.png": "src/images/proof-maintenance-cost.png",
            "spec-drift-vs-test-coverage.png": "src/images/spec-drift-vs-test-coverage.png",
            "governance-process-latency.png": "src/images/governance-process-latency.png",
            "multisig-threshold-sensitivity.png": "src/images/multisig-threshold-sensitivity.png",
        }
        for name, old in previous.items():
            blob = subprocess.check_output(["git", "show", f"HEAD:{old}"], cwd=ROOT)
            carried = (ROOT / "charts" / "carried" / name).read_bytes()
            self.assertEqual(hashlib.sha256(blob).digest(), hashlib.sha256(carried).digest(), name)
        radar = (ROOT / "charts" / "carried" / "consensus-coverage.png").read_bytes()
        website = Path(
            "/mnt/data/bitcoin/blvm/commons-website/assets/images/Consensus-Coverage-Comparison.png"
        ).read_bytes()
        self.assertEqual(hashlib.sha256(radar).digest(), hashlib.sha256(website).digest())

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
