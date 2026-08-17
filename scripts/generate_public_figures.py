from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)


def save(fig, filename):
    path = FIGURES / filename
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("CREATED", path.relative_to(ROOT))


# ------------------------------------------------------------------
# 1. Original validation failure
# ------------------------------------------------------------------

failed = pd.read_csv(TABLES / "failed_validation_summary.csv").copy()

labels = (
    failed["candidate"]
    .replace({
        "momentum_immediate": "MOM",
        "momentum_delayed_1d": "MOMD",
    })
)

fig, ax = plt.subplots(figsize=(7.5, 4.8))
ax.bar(labels, failed["net_sharpe_20bps"])
ax.axhline(0.0, linestyle="--", linewidth=1)
ax.set_title("Frozen 2023–2024 Validation Failure")
ax.set_ylabel("Annualized net Sharpe at 20 bps")
save(fig, "01_failed_validation.png")


# ------------------------------------------------------------------
# 2. Continuation redesign — formation economics
# ------------------------------------------------------------------

formation = pd.read_csv(
    TABLES / "continuation_formation_summary.csv"
).copy()

if "window" in formation.columns:
    formation = formation.loc[formation["window"].eq("evaluation")]

formation_order = ["12h", "1d", "2d", "3d", "1w", "2w", "1m", "3m"]

fig, ax = plt.subplots(figsize=(9, 5))
for mapping, group in formation.groupby("portfolio_mapping"):
    group = group.copy()
    group["formation_horizon"] = pd.Categorical(
        group["formation_horizon"],
        categories=formation_order,
        ordered=True,
    )
    group = group.sort_values("formation_horizon")

    ax.plot(
        group["formation_horizon"].astype(str),
        group["median_break_even_bps"],
        marker="o",
        label=mapping,
    )

ax.axhline(20.0, linestyle="--", linewidth=1, label="20 bps threshold")
ax.set_title("Pre-2025 Continuation Redesign")
ax.set_xlabel("Formation horizon")
ax.set_ylabel("Median break-even execution cost (bps)")
ax.legend()
save(fig, "02_continuation_formation_economics.png")


# ------------------------------------------------------------------
# 3. Untouched final holdout — economics
# ------------------------------------------------------------------

holdout = pd.read_csv(TABLES / "final_holdout_metrics.csv").copy()
order = ["ECON", "BAL", "SHARP"]
holdout["finalist"] = pd.Categorical(
    holdout["finalist"], categories=order, ordered=True
)
holdout = holdout.sort_values("finalist")

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(
    holdout["finalist"].astype(str),
    holdout["break_even_cost_bps"],
)
ax.axhline(20.0, linestyle="--", linewidth=1, label="Primary cost = 20 bps")
ax.set_title("Untouched Final Holdout — Execution-Cost Headroom")
ax.set_ylabel("Break-even execution cost (bps)")
ax.legend()
save(fig, "03_final_holdout_break_even.png")


# ------------------------------------------------------------------
# 4. Execution-cost sensitivity
# ------------------------------------------------------------------

cost = pd.read_csv(TABLES / "cost_sensitivity_summary.csv").copy()

required_cost_cols = {
    "gross_sharpe": 0,
    "net7_sharpe": 7,
    "net20_sharpe": 20,
    "net40_sharpe": 40,
}

if all(col in cost.columns for col in required_cost_cols):
    fig, ax = plt.subplots(figsize=(9, 5))

    for finalist in order:
        row = cost.loc[cost["finalist"].eq(finalist)].iloc[0]
        x = list(required_cost_cols.values())
        y = [float(row[col]) for col in required_cost_cols]
        ax.plot(x, y, marker="o", label=finalist)

    ax.axvline(20.0, linestyle="--", linewidth=1)
    ax.axhline(0.0, linestyle="--", linewidth=1)
    ax.set_title("Untouched Holdout — Sharpe vs Execution Cost")
    ax.set_xlabel("Cost per unit of full-L1 turnover (bps)")
    ax.set_ylabel("Annualized Sharpe")
    ax.legend()

    save(fig, "04_cost_sensitivity.png")
else:
    print("SKIPPED 04_cost_sensitivity.png — unexpected table schema")


# ------------------------------------------------------------------
# 5. Realized downside risk
# ------------------------------------------------------------------

risk = pd.read_csv(TABLES / "risk_tail_summary.csv").copy()
risk["finalist"] = pd.Categorical(
    risk["finalist"], categories=order, ordered=True
)
risk = risk.sort_values("finalist")

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(
    risk["finalist"].astype(str),
    100.0 * risk["max_drawdown"],
)
ax.axhline(0.0, linestyle="--", linewidth=1)
ax.set_title("Untouched Holdout — Net-20 Maximum Drawdown")
ax.set_ylabel("Maximum drawdown (%)")
save(fig, "05_final_holdout_drawdown.png")


# ------------------------------------------------------------------
# 6. Asset contribution concentration
# ------------------------------------------------------------------

conc = pd.read_csv(
    TABLES / "asset_concentration_summary.csv"
).copy()
conc["finalist"] = pd.Categorical(
    conc["finalist"], categories=order, ordered=True
)
conc = conc.sort_values("finalist")

x = np.arange(len(conc))
width = 0.34

fig, ax = plt.subplots(figsize=(8.5, 5))
ax.bar(
    x - width / 2,
    conc["largest_single_name_share_pct"],
    width,
    label="Largest single asset",
)
ax.bar(
    x + width / 2,
    conc["top5_absolute_share_pct"],
    width,
    label="Top 5 assets",
)

ax.set_xticks(x)
ax.set_xticklabels(conc["finalist"].astype(str))
ax.set_title("Untouched Holdout — Contribution Concentration")
ax.set_ylabel("Share of absolute P&L contribution (%)")
ax.legend()
save(fig, "06_asset_concentration.png")


print()
print("PUBLIC FIGURE GENERATION COMPLETE")
