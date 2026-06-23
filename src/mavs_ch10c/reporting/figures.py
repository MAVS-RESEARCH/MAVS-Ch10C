"""Phase 5 stability and variance figure builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.reporting import GOVERNANCE_SYSTEMS, REQUIRED_FIGURES
from mavs_ch10c.reporting.tables import build_report_tables
from mavs_ch10c.verification.hash_utils import sha256_file

FIGURE_DPI = 160
RUN_MODE_COLORS = {
    "locked": "#2f5d8c",
    "audit": "#8a5a2b",
}


def build_stability_figures(
    repo_root: Path,
    config: dict[str, Any],
    tables: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Path]:
    """Build all required Phase 5 PNG figures."""

    # console.log: phase5 stability figure build begins.
    console.log("phase5.figures.build.start")
    tables = tables or build_report_tables(repo_root, config)
    variance = pd.DataFrame(tables["variance_tables"])
    stability = pd.DataFrame(tables["stability_tables"])
    outputs = {
        "accuracy_variance_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["accuracy_variance_by_system"],
            variance[variance["metric_name"] == "accuracy_variance"],
            value_field="sample_variance",
            title="Accuracy Variance by System",
            ylabel="Mean sample variance",
            systems=config["expected"]["systems"],
        ),
        "f1_variance_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["f1_variance_by_system"],
            variance[variance["metric_name"] == "f1_variance"],
            value_field="sample_variance",
            title="F1 Variance by System",
            ylabel="Mean sample variance",
            systems=config["expected"]["systems"],
        ),
        "prediction_stability_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["prediction_stability_by_system"],
            stability[stability["metric_name"] == "prediction_stability"],
            value_field="reported_value",
            title="Prediction Stability by System",
            ylabel="Mean pairwise agreement",
            systems=config["expected"]["systems"],
        ),
        "decision_stability_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["decision_stability_by_system"],
            stability[stability["metric_name"] == "decision_stability"],
            value_field="reported_value",
            title="Decision Stability by System",
            ylabel="Mean governed decision agreement",
            systems=config["expected"]["systems"],
        ),
        "consensus_stability_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["consensus_stability_by_system"],
            stability[stability["metric_name"] == "consensus_stability"],
            value_field="reported_value",
            title="Consensus or Score Stability by System",
            ylabel="Mean pairwise stability",
            systems=config["expected"]["systems"],
        ),
        "trace_stability_by_system": _render_system_bars(
            repo_root / config["figure_paths"]["trace_stability_by_system"],
            stability[stability["metric_name"] == "trace_stability"],
            value_field="reported_value",
            title="Trace Stability by Governance System",
            ylabel="Mean normalized trace similarity",
            systems=GOVERNANCE_SYSTEMS,
        ),
        "confidence_interval_widths": _render_system_bars(
            repo_root / config["figure_paths"]["confidence_interval_widths"],
            variance,
            value_field="confidence_interval_width",
            title="Confidence Interval Width by System",
            ylabel="Mean analytical interval width",
            systems=config["expected"]["systems"],
        ),
    }
    missing = [name for name in REQUIRED_FIGURES if name not in outputs or not outputs[name].exists()]
    if missing:
        raise RuntimeError(f"Missing required figures: {missing}")
    # console.log: phase5 stability figure build completed.
    console.log(f"phase5.figures.build.complete figures={len(outputs)}")
    return outputs


def figure_hashes(repo_root: Path, config: dict[str, Any]) -> dict[str, str]:
    """Return SHA-256 hashes for generated figures."""

    return {
        name: sha256_file(repo_root / config["figure_paths"][name])
        for name in REQUIRED_FIGURES
    }


def _render_system_bars(
    path: Path,
    frame: pd.DataFrame,
    value_field: str,
    title: str,
    ylabel: str,
    systems: list[str],
) -> Path:
    # console.log: phase5 individual figure render begins.
    console.log(f"phase5.figures.render.start path={path}")
    data = frame.copy()
    if data.empty:
        raise RuntimeError(f"No rows available for figure {path}")
    data = data[data["system_id"].isin(systems)].copy()
    data[value_field] = pd.to_numeric(data[value_field], errors="coerce")
    data = data.dropna(subset=[value_field])
    if data.empty:
        raise RuntimeError(f"No numeric values available for figure {path}")
    grouped = (
        data.groupby(["system_id", "run_mode"], as_index=False)[value_field]
        .mean()
        .rename(columns={value_field: "value"})
    )
    grouped["system_id"] = pd.Categorical(grouped["system_id"], categories=systems, ordered=True)
    grouped = grouped.sort_values(["system_id", "run_mode"])
    pivot = grouped.pivot(index="system_id", columns="run_mode", values="value").reindex(systems)
    pivot = pivot.dropna(how="all")
    if pivot.empty:
        raise RuntimeError(f"No plotted groups available for figure {path}")

    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    x_positions = list(range(len(pivot.index)))
    bar_width = 0.36
    run_modes = [mode for mode in ["locked", "audit"] if mode in pivot.columns]
    offsets = _bar_offsets(len(run_modes), bar_width)
    for offset, run_mode in zip(offsets, run_modes, strict=True):
        values = pivot[run_mode].fillna(0.0).to_list()
        ax.bar(
            [position + offset for position in x_positions],
            values,
            width=bar_width,
            color=RUN_MODE_COLORS[run_mode],
            label=run_mode,
        )
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("System")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([_display_system(system) for system in pivot.index], rotation=25, ha="right")
    ax.grid(axis="y", linestyle=":", linewidth=0.7, alpha=0.7)
    ax.legend(title="Run mode", frameon=False)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=FIGURE_DPI, metadata={"Software": "MAVS-Ch10C Phase5"})
    plt.close(fig)
    # console.log: phase5 individual figure render completed.
    console.log(f"phase5.figures.render.complete path={path}")
    return path


def _bar_offsets(count: int, width: float) -> list[float]:
    if count == 1:
        return [0.0]
    center = (count - 1) / 2
    return [(index - center) * width for index in range(count)]


def _display_system(system_id: str) -> str:
    return system_id.replace("_", " ").title()
