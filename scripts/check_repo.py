from pathlib import Path
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "pyproject.toml",
    ".gitignore",

    "docs/research_history.md",
    "docs/methodology.md",
    "docs/reproducibility.md",

    "data/README.md",
    "data/universe/monthly_universe.csv",
    "data/universe/research_symbols.csv",

    "results/README.md",
    "results/tables/frozen_finalists.csv",
    "results/tables/failed_validation_summary.csv",
    "results/tables/final_holdout_protocol.json",
    "results/tables/final_holdout_metrics.csv",

    "notebooks/01_data_and_universe.ipynb",
    "notebooks/02_signal_research.ipynb",
    "notebooks/03_portfolio_construction_and_failed_validation.ipynb",
    "notebooks/04_failure_diagnosis_and_continuation_redesign.ipynb",
    "notebooks/05_untouched_final_holdout.ipynb",
    "notebooks/06_final_risk_and_robustness.ipynb",

    "src/crypto_alpha/__init__.py",
    "src/crypto_alpha/config.py",
    "src/crypto_alpha/io.py",
    "src/crypto_alpha/metrics.py",
    "src/crypto_alpha/portfolio.py",
    "src/crypto_alpha/signals.py",

    "tests/test_metrics.py",
    "tests/test_portfolio.py",
    "tests/test_frozen_research.py",
]

PRIVATE_PATTERNS = [
    "data/raw",
    "data/processed",
    "data/processed_1h",
    "data/processed_1h_step12_holdout",
    "research_cache",
]

print("=" * 88)
print("PUBLIC REPOSITORY SAFETY AUDIT")
print("=" * 88)
print("Root:", ROOT)

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("\nMISSING REQUIRED FILES:")
    for p in missing:
        print("  ", p)
    sys.exit(1)

for pattern in PRIVATE_PATTERNS:
    path = ROOT / pattern
    if path.exists():
        raise RuntimeError(
            f"Private/large data location exists in public repo: {path}"
        )

# Universe invariants
u = pd.read_csv(ROOT / "data/universe/monthly_universe.csv")
u["effective_month"] = pd.to_datetime(u["effective_month"], utc=True)

assert u["effective_month"].nunique() == 76
assert u["symbol"].nunique() == 151
assert (
    u.groupby("effective_month")["symbol"]
    .nunique()
    .eq(25)
    .all()
)

# Failed validation must remain failed
failed = pd.read_csv(
    ROOT / "results/tables/failed_validation_summary.csv"
)
assert (failed["mean_net_return_20bps"] < 0).all()
assert (failed["net_sharpe_20bps"] < 0).all()
assert (failed["break_even_bps"] < 20).all()

# Final holdout must remain frozen 3/3 pass
final = pd.read_csv(
    ROOT / "results/tables/final_holdout_metrics.csv"
)
assert set(final["finalist"]) == {"ECON", "BAL", "SHARP"}
assert (final["mean_price_ic"] > 0).all()
assert (final["gross_ann_return"] > 0).all()
assert (final["break_even_cost_bps"] >= 20).all()

with open(
    ROOT / "results/tables/final_holdout_protocol.json",
    "r",
    encoding="utf-8",
) as f:
    protocol = json.load(f)

assert protocol["holdout_start"] == "2025-01-01 00:00:00+00:00"
assert protocol["holdout_end_exclusive"] == "2026-08-01 00:00:00+00:00"
assert float(protocol["primary_cost_bps"]) == 20.0
assert protocol["combined_portfolio"] is False

# Basic large-file check
large_files = []
for path in ROOT.rglob("*"):
    if path.is_file() and ".venv" not in path.parts:
        mb = path.stat().st_size / (1024 ** 2)
        if mb > 10:
            large_files.append((path.relative_to(ROOT), mb))

print("\nRequired repository files: PASS")
print("Point-in-time universe invariants: PASS")
print("Original validation remains failure: PASS")
print("Frozen final holdout remains 3/3 pass: PASS")
print("Private raw/processed data directories absent: PASS")

if large_files:
    print("\nWARNING — files over 10 MB:")
    for path, mb in large_files:
        print(f"  {path}: {mb:.2f} MB")
else:
    print("Unexpected files >10 MB: NONE")

print("\nPUBLIC REPOSITORY SAFETY AUDIT: PASS")
