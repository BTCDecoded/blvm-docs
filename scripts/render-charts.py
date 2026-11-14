#!/usr/bin/env python3
"""Rebuild the manual's charts from governance YAML and charts/catalog.yml.

Writes SVG and Mermaid fragments. `--check` fails when the committed
fragments differ, which is what CI runs. A `series` chart stays an empty
panel until `charts/series/<id>.yml` is measured, dated, and sourced.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "charts" / "catalog.yml"

LAYER_KEYS = (
    "layer_1_constitutional",
    "layer_2_constitutional",
    "layer_3_implementation",
    "layer_4_application",
    "layer_5_extension",
)
TIER_KEYS = (
    ("tier_1_routine", "T1 Routine"),
    ("tier_2_features", "T2 Features"),
    ("tier_3_consensus_adjacent", "T3 Consensus-adjacent"),
    ("tier_4_emergency", "T4 Emergency"),
    ("tier_5_governance", "T5 Governance"),
)
LAYER_SHORT = ("L1 spec", "L2 consensus", "L3 protocol", "L4 node", "L5 sdk")

INK = "#1c1915"
MUTED = "#5c564c"
GRID = "#e4ddd0"
PAPER = "#fbfaf7"
REQUIRED = "#1d4e89"
TOTAL = "#0e7c66"
REVIEW = "#c44900"
CONSENSUS = "#5c4d7a"
CURVE_COLORS = ("#1d4e89", "#c44900", "#0e7c66", "#6b3fa0", "#9a3412")


def load_catalog() -> list[dict]:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    charts = data.get("charts")
    if not isinstance(charts, list) or not charts:
        raise SystemExit("charts/catalog.yml has no charts")
    return charts


def load_layers() -> list[dict]:
    path = ROOT / "modules/governance/config/repository-layers.yml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["layers"]
    layers = []
    for key, short in zip(LAYER_KEYS, LAYER_SHORT):
        row = raw[key]
        layers.append(
            {
                "key": key,
                "short": short,
                "required": int(row["signatures"]["required"]),
                "total": int(row["signatures"]["total"]),
                "review": int(row["review_period_days"]),
                "consensus_review": (
                    int(row["consensus_review_period_days"])
                    if "consensus_review_period_days" in row
                    else None
                ),
            }
        )
    return layers


def load_tiers() -> list[dict]:
    path = ROOT / "modules/governance/config/action-tiers.yml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["tiers"]
    tiers = []
    for key, label in TIER_KEYS:
        row = raw[key]
        tiers.append({"key": key, "label": label, "days": int(row["review_period_days"])})
    return tiers


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_open(width: int, height: int, title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" width="{width}" height="{height}">',
        f"<title>{esc(title)}</title>",
        f"<desc>{esc(desc)}</desc>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]


def wrap(text: str, limit: int = 78) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and len(trial) > limit:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines


def empty_panel(title: str, measure: str, unit: str) -> str:
    lines = wrap(measure)
    height = 148 + 22 * len(lines)
    parts = svg_open(720, height, title, measure)
    parts.append(
        f'<text x="32" y="40" fill="{INK}" font-family="system-ui,sans-serif" '
        f'font-size="20" font-weight="650">{esc(title)}</text>'
    )
    y = 72
    for line in lines:
        parts.append(
            f'<text x="32" y="{y}" fill="{MUTED}" font-family="system-ui,sans-serif" '
            f'font-size="15">{esc(line)}</text>'
        )
        y += 22
    parts.append(
        f'<text x="32" y="{y + 8}" fill="{INK}" font-family="system-ui,sans-serif" '
        f'font-size="16" font-weight="650">No series is published.</text>'
    )
    parts.append(
        f'<text x="32" y="{y + 32}" fill="{MUTED}" font-family="system-ui,sans-serif" '
        f'font-size="13">Unit: {esc(unit)}</text>'
    )
    parts.append("</svg>\n")
    return "\n".join(parts)


def y_scale(value: float, y_max: float, top: int, height: int) -> float:
    if y_max <= 0:
        return float(top + height)
    return top + height - (value / y_max) * height


def axis_ceiling(y_max: float) -> float:
    """Round the axis up so ticks land on whole numbers."""
    if y_max <= 0:
        return 1
    if y_max <= 8:
        return float(math.ceil(y_max))
    raw = y_max / 4
    magnitude = 10 ** math.floor(math.log10(raw))
    step = 10 * magnitude
    for factor in (1, 2, 2.5, 5, 10):
        candidate = factor * magnitude
        if candidate >= raw - 1e-9:
            step = candidate
            break
    return math.ceil((y_max - 1e-9) / step) * step


def axis_ticks(ceiling: float) -> list[float]:
    if ceiling <= 8:
        return [float(i) for i in range(int(ceiling) + 1)]
    step = ceiling / 4
    return [i * step for i in range(5)]


def format_tick(value: float) -> str:
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.2f}"


def grouped_bars(
    title: str,
    desc: str,
    categories: list[str],
    series: list[dict],
    y_max: float,
    y_label: str,
    footnote: str,
) -> str:
    width, height = 760, 360
    left, right, top, bottom = 78, 20, 64, 108
    plot_w = width - left - right
    plot_h = height - top - bottom
    ceiling = axis_ceiling(y_max)
    parts = svg_open(width, height, title, desc)
    parts.append(
        f'<text x="32" y="32" fill="{INK}" font-family="system-ui,sans-serif" '
        f'font-size="18" font-weight="650">{esc(title)}</text>'
    )
    parts.append(
        f'<text x="18" y="{top + plot_h / 2}" fill="{MUTED}" '
        f'font-family="system-ui,sans-serif" font-size="12" text-anchor="middle" '
        f'transform="rotate(-90 18 {top + plot_h / 2})">{esc(y_label)}</text>'
    )
    for val in axis_ticks(ceiling):
        y = y_scale(val, ceiling, top, plot_h)
        parts.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="{GRID}"/>'
        )
        parts.append(
            f'<text x="{left - 8}" y="{y + 4:.1f}" fill="{MUTED}" text-anchor="end" '
            f'font-family="system-ui,sans-serif" font-size="12">{format_tick(val)}</text>'
        )
    n_cat = len(categories)
    n_ser = len(series)
    group_w = plot_w / n_cat
    bar_w = min(22, (group_w * 0.7) / n_ser)
    for c, name in enumerate(categories):
        gx = left + c * group_w + (group_w - n_ser * bar_w) / 2
        for s, item in enumerate(series):
            value = item["values"][c]
            if value is None:
                continue
            y = y_scale(value, ceiling, top, plot_h)
            base = top + plot_h
            h = max(0.0, base - y)
            x = gx + s * bar_w
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w - 3:.1f}" height="{h:.1f}" '
                f'fill="{item["color"]}"/>'
            )
            shown = str(int(value)) if float(value).is_integer() else f"{value:.2f}"
            parts.append(
                f'<text x="{x + (bar_w - 3) / 2:.1f}" y="{y - 4:.1f}" fill="{INK}" '
                f'text-anchor="middle" font-family="system-ui,sans-serif" font-size="11">{shown}</text>'
            )
        parts.append(
            f'<text x="{left + c * group_w + group_w / 2:.1f}" y="{top + plot_h + 20}" '
            f'fill="{INK}" text-anchor="middle" font-family="system-ui,sans-serif" '
            f'font-size="12">{esc(name)}</text>'
        )
    legend_x = left
    for item in series:
        parts.append(f'<rect x="{legend_x}" y="{height - 58}" width="12" height="12" fill="{item["color"]}"/>')
        parts.append(
            f'<text x="{legend_x + 18}" y="{height - 48}" fill="{INK}" '
            f'font-family="system-ui,sans-serif" font-size="12">{esc(item["name"])}</text>'
        )
        legend_x += 18 + 8 * len(item["name"]) + 28
    parts.append(
        f'<text x="32" y="{height - 22}" fill="{MUTED}" font-family="system-ui,sans-serif" '
        f'font-size="12">{esc(footnote)}</text>'
    )
    parts.append("</svg>\n")
    return "\n".join(parts)


def layer_chart(layers: list[dict]) -> str:
    cats = [row["short"] for row in layers]
    sig = grouped_bars(
        "Signatures by repository layer",
        "Required signatures and maintainer set size from repository-layers.yml.",
        cats,
        [
            {"name": "Required", "color": REQUIRED, "values": [r["required"] for r in layers]},
            {"name": "Set size", "color": TOTAL, "values": [r["total"] for r in layers]},
        ],
        y_max=max(r["total"] for r in layers),
        y_label="signatures",
        footnote="From repository-layers.yml. Counts are the published policy, not observed signatures.",
    )
    days_values = []
    consensus_values = []
    for row in layers:
        days_values.append(row["review"])
        consensus_values.append(row["consensus_review"])
    y_max = max([v for v in days_values + consensus_values if v is not None])
    days = grouped_bars(
        "Review window by repository layer",
        "Published review windows from repository-layers.yml. Consensus-change windows exist only for layers 1 and 2.",
        cats,
        [
            {"name": "Review days", "color": REVIEW, "values": days_values},
            {"name": "Consensus-change days", "color": CONSENSUS, "values": consensus_values},
        ],
        y_max=y_max,
        y_label="days",
        footnote="Policy windows. Not a measured review duration.",
    )
    # Stack the two SVGs in one file by dropping the second XML declaration-less root
    # and placing both panels in a taller canvas. Rebuild as one SVG instead.
    return _stack_svgs(
        "Signature thresholds by repository layer",
        "Required signatures, set size, and review windows from repository-layers.yml.",
        sig,
        days,
    )


def _inner(svg: str) -> str:
    title = svg.find("<text ")
    end = svg.rfind("</svg>")
    return svg[title:end]


def _stack_svgs(title: str, desc: str, top_svg: str, bottom_svg: str) -> str:
    # Each panel SVG is 760x360. Place them in one 760x700 canvas with a shared title strip removed
    # by cropping the panel titles which are already inside.
    width, height = 760, 720
    parts = svg_open(width, height, title, desc)
    parts.append(f'<g transform="translate(0 0)">{_inner(top_svg)}</g>')
    parts.append(f'<g transform="translate(0 360)">{_inner(bottom_svg)}</g>')
    parts.append("</svg>\n")
    return "\n".join(parts)


def tier_chart(tiers: list[dict]) -> str:
    y_max = max(row["days"] for row in tiers) or 1
    return grouped_bars(
        "Review period by action tier",
        "Published review period in days for action tiers 1 through 5.",
        [row["label"] for row in tiers],
        [{"name": "Review days", "color": REVIEW, "values": [row["days"] for row in tiers]}],
        y_max=y_max,
        y_label="days",
        footnote="From action-tiers.yml. The emergency tier is zero days. Not a measured pull-request time.",
    )


def binom_at_least(n: int, k: int, p: float) -> float:
    if p <= 0:
        return 1.0 if k <= 0 else 0.0
    if p >= 1:
        return 1.0 if n >= k else 0.0
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * (p**i) * ((1 - p) ** (n - i))
    return total


def quorum_groups(layers: list[dict]) -> list[dict]:
    groups: list[dict] = []
    for row in layers:
        key = (row["required"], row["total"])
        found = next((g for g in groups if g["key"] == key), None)
        if found:
            found["labels"].append(row["short"])
        else:
            groups.append({"key": key, "labels": [row["short"]]})
    for group in groups:
        k, n = group["key"]
        names = " and ".join(group["labels"])
        group["name"] = f"{names}, {k} of {n}"
    return groups


def quorum_chart(layers: list[dict]) -> str:
    groups = quorum_groups(layers)
    width, height = 760, 480
    left, right, top, bottom = 64, 24, 56, 150
    plot_w = width - left - right
    plot_h = height - top - bottom
    desc = (
        "Model: each signer is compromised independently with probability p. "
        "The curve is P(X ≥ required) for the k and n in repository-layers.yml. "
        "p is not a measured attacker rate."
    )
    parts = svg_open(width, height, "Quorum capture probability", desc)
    parts.append(
        f'<text x="32" y="32" fill="{INK}" font-family="system-ui,sans-serif" '
        f'font-size="18" font-weight="650">Quorum capture probability</text>'
    )
    for i in range(5):
        val = i / 4
        y = y_scale(val, 1, top, plot_h)
        x = left + val * plot_w
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="{GRID}"/>')
        parts.append(
            f'<text x="{left - 8}" y="{y + 4:.1f}" fill="{MUTED}" text-anchor="end" '
            f'font-family="system-ui,sans-serif" font-size="12">{val:.2f}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{top + plot_h + 18}" fill="{MUTED}" text-anchor="middle" '
            f'font-family="system-ui,sans-serif" font-size="12">{val:.2f}</text>'
        )
    parts.append(
        f'<text x="{left + plot_w / 2:.1f}" y="{top + plot_h + 38}" fill="{MUTED}" '
        f'text-anchor="middle" font-family="system-ui,sans-serif" font-size="12">'
        f"per-signer compromise probability p</text>"
    )
    steps = [i / 20 for i in range(21)]
    for index, group in enumerate(groups):
        k, n = group["key"]
        color = CURVE_COLORS[index % len(CURVE_COLORS)]
        points = []
        for p in steps:
            x = left + p * plot_w
            y = y_scale(binom_at_least(n, k, p), 1, top, plot_h)
            points.append(f"{x:.1f},{y:.1f}")
        parts.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{" ".join(points)}"/>'
        )
        parts.append(
            f'<rect x="{left + (index % 2) * 340}" y="{height - 64 - (index // 2) * 22}" '
            f'width="12" height="12" fill="{color}"/>'
        )
        parts.append(
            f'<text x="{left + 18 + (index % 2) * 340}" y="{height - 54 - (index // 2) * 22}" '
            f'fill="{INK}" font-family="system-ui,sans-serif" font-size="12">{esc(group["name"])}</text>'
        )
    parts.append("</svg>\n")
    return "\n".join(parts)


def series_path(chart_id: str) -> Path:
    return ROOT / "charts" / "series" / f"{chart_id}.yml"


def load_series(chart_id: str) -> dict | None:
    path = series_path(chart_id)
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} is not a mapping")
    status = data.get("status")
    if status == "unmeasured":
        return None
    if status not in ("measured", "carried"):
        raise SystemExit(f"{path} status must be measured, carried, or unmeasured")
    for key in ("measured_at", "source", "unit", "categories", "series"):
        if key not in data or data[key] in (None, "", []):
            raise SystemExit(f"{path} measured series is missing {key}")
    categories = data["categories"]
    if not isinstance(categories, list) or not categories:
        raise SystemExit(f"{path} categories must be a non-empty list")
    for item in data["series"]:
        values = item.get("values")
        if not isinstance(values, list) or len(values) != len(categories):
            raise SystemExit(f"{path} series {item.get('name')} must match categories")
        item["values"] = [float(v) for v in values]
    return data


def series_chart(chart: dict) -> str:
    measured = load_series(chart["id"])
    if measured is None:
        return empty_panel(chart["title"], chart["measure"], chart["unit"])
    y_max = max(v for item in measured["series"] for v in item["values"]) or 1
    colors = (REQUIRED, TOTAL, REVIEW, CONSENSUS, CURVE_COLORS[4])
    series = []
    for index, item in enumerate(measured["series"]):
        series.append(
            {
                "name": str(item["name"]),
                "color": colors[index % len(colors)],
                "values": item["values"],
            }
        )
    label = "Carried" if measured.get("status") == "carried" else "Measured"
    footnote = f"{label} {measured['measured_at']}. Source: {measured['source']}."
    return grouped_bars(
        chart["title"],
        f"{chart['measure']} Unit: {measured['unit']}. {footnote}",
        [str(c) for c in measured["categories"]],
        series,
        y_max=y_max,
        y_label=str(measured["unit"]),
        footnote=footnote,
    )


def mermaid_fragment(chart: dict) -> str:
    body = chart["diagram"].strip("\n")
    return f"```mermaid\n{body}\n```\n"


CELL = {"complete": "#0e7c66", "partial": "#c44900", "absent": "#9b2335"}


def load_matrix(chart_id: str) -> dict:
    path = series_path(chart_id)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data.get("status") != "carried":
        raise SystemExit(f"{path} matrix must be status carried")
    for key in ("measured_at", "source", "categories", "rows"):
        if not data.get(key):
            raise SystemExit(f"{path} matrix is missing {key}")
    width = len(data["categories"])
    for row in data["rows"]:
        if len(row["values"]) != width:
            raise SystemExit(f"{path} row {row.get('name')} does not match categories")
        for value in row["values"]:
            if value not in CELL:
                raise SystemExit(f"{path} value {value} is not complete, partial, or absent")
    return data


def matrix_chart(chart: dict) -> str:
    data = load_matrix(chart["id"])
    categories = [str(c) for c in data["categories"]]
    rows = data["rows"]
    label_w, cell, gap = 210, 108, 8
    width = 32 + label_w + len(categories) * (cell + gap)
    height = 96 + len(rows) * 36 + 56
    desc = f"{chart['measure']} Carried {data['measured_at']}. Source: {data['source']}."
    parts = svg_open(width, height, chart["title"], desc)
    parts.append(
        f'<text x="24" y="32" fill="{INK}" font-family="system-ui,sans-serif" '
        f'font-size="18" font-weight="650">{esc(chart["title"])}</text>'
    )
    for i, name in enumerate(categories):
        x = 24 + label_w + i * (cell + gap) + cell / 2
        parts.append(
            f'<text x="{x:.0f}" y="68" fill="{INK}" text-anchor="middle" '
            f'font-family="system-ui,sans-serif" font-size="12">{esc(name)}</text>'
        )
    for r, row in enumerate(rows):
        y = 84 + r * 36
        parts.append(
            f'<text x="24" y="{y + 16}" fill="{INK}" font-family="system-ui,sans-serif" '
            f'font-size="13">{esc(row["name"])}</text>'
        )
        for i, value in enumerate(row["values"]):
            x = 24 + label_w + i * (cell + gap)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="26" rx="4" fill="{CELL[value]}"/>'
            )
            parts.append(
                f'<text x="{x + cell / 2:.0f}" y="{y + 17}" fill="#fbfaf7" text-anchor="middle" '
                f'font-family="system-ui,sans-serif" font-size="12">{esc(value)}</text>'
            )
    parts.append(
        f'<text x="24" y="{height - 18}" fill="{MUTED}" font-family="system-ui,sans-serif" '
        f'font-size="12">Carried {esc(data["measured_at"])}. {esc(data["source"])}</text>'
    )
    parts.append("</svg>\n")
    return "\n".join(parts)


def render_chart(chart: dict, layers: list[dict], tiers: list[dict]) -> str | None:
    kind = chart["kind"]
    if kind == "carried":
        source = ROOT / chart["source"]
        if not source.is_file() or source.stat().st_size < 1000:
            raise SystemExit(f"carried chart {chart['id']} is missing {chart['source']}")
        return None
    if kind == "layer-thresholds":
        return layer_chart(layers)
    if kind == "tier-review":
        return tier_chart(tiers)
    if kind == "quorum-curves":
        return quorum_chart(layers)
    if kind == "mermaid":
        return mermaid_fragment(chart)
    if kind == "series":
        return series_chart(chart)
    if kind == "matrix":
        return matrix_chart(chart)
    raise SystemExit(f"unknown chart kind {kind} on {chart.get('id')}")


def outputs() -> dict[Path, str]:
    layers = load_layers()
    tiers = load_tiers()
    rendered = {}
    for chart in load_catalog():
        text = render_chart(chart, layers, tiers)
        if text is None:
            continue
        path = ROOT / chart["output"]
        rendered[path] = text
    return rendered


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed charts are stale")
    args = parser.parse_args(argv)
    stale = []
    for path, text in outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if args.check:
            if current != text:
                stale.append(path.relative_to(ROOT).as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if stale:
        print("stale charts (run python3 scripts/render-charts.py):", file=sys.stderr)
        for name in stale:
            print(f"  {name}", file=sys.stderr)
        return 1
    if args.check:
        print(f"render-charts: {len(outputs())} charts match")
    else:
        print(f"render-charts: wrote {len(outputs())} charts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
