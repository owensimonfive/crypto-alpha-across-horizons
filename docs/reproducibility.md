# Reproducibility

## Two reproducibility modes

This repository supports two different levels of review.

### 1. Lightweight reviewer mode

A reviewer can inspect the six public notebooks, the point-in-time universe files, and the small frozen result artifacts without downloading the full Binance dataset.

This is the intended GitHub/recruiter workflow.

The repository includes:

- `data/universe/`
- `results/tables/`
- `notebooks/`
- curated figures once generated

The large raw and processed datasets are intentionally excluded.

### 2. Full rebuild mode

A full rebuild requires historical Binance market data and the canonical acquisition / processing pipeline.

The public repository will expose the reusable logic required to regenerate the research, but it will not distribute years of raw exchange bars.

## Environment

Recommended Python:

```text
Python 3.11–3.13
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[notebooks]"
```

Core dependencies are declared in `pyproject.toml`.

## Public notebook order

Run the notebooks in this order:

```text
01_data_and_universe.ipynb
02_signal_research.ipynb
03_portfolio_construction_and_failed_validation.ipynb
04_failure_diagnosis_and_continuation_redesign.ipynb
05_untouched_final_holdout.ipynb
06_final_risk_and_robustness.ipynb
```

The notebooks are ordered by research logic.

## Important note about frozen artifacts

Some public notebooks intentionally load small frozen result tables produced by the canonical historical engines instead of recomputing every expensive grid from raw bars.

This is deliberate.

The project distinguishes between:

- **research argument and verification**, which belongs in the public notebooks;
- **heavy mechanical grid execution**, which belongs in reusable shared code;
- **large intermediate caches**, which do not belong in GitHub.

Where a notebook loads a frozen artifact, it also performs integrity checks or reconstructs decisive summary statistics from lower-level saved paths when practical.

## Data directory

The public repository includes only small universe metadata:

```text
data/universe/monthly_universe.csv
data/universe/research_symbols.csv
```

Raw and processed market bars are excluded.

## Result artifacts

`results/tables/` contains small frozen artifacts used to document and verify the research record, including:

- failed validation summary;
- continuation horizon summaries;
- frozen finalists;
- frozen final-holdout protocol;
- pre-2025 reproduction gate;
- final holdout metrics;
- holdout degradation;
- finalist correlations;
- cost sensitivity;
- risk/tail summary;
- monthly breadth;
- market exposure;
- implementation breadth;
- asset concentration.

These files are intentionally small enough for direct GitHub inspection.

## Expected research invariants

A correct rebuild should preserve the following high-level invariants:

### Universe

- 76 monthly snapshots;
- 25 assets per month;
- 151 unique research symbols.

### Original validation

The 2023–2024 Cycle-A momentum validation must remain a failure.

### Frozen continuation finalists

- ECON: continuous rank, 2w formation, 6w holding, 24h cadence;
- BAL: equal-weight terciles, 3d formation, 8w holding, 48h cadence;
- SHARP: equal-weight terciles, 1d formation, 8w holding, 8h cadence.

### Final holdout

The untouched holdout is:

```text
2025-01-01 00:00 UTC
through
2026-08-01 00:00 UTC exclusive
```

All three finalists must satisfy the frozen survival rule.

Approximate headline values:

| Finalist | Gross Sharpe | Net-20 Sharpe | Break-even |
|---|---:|---:|---:|
| ECON | 0.334 | 0.099 | 28.50 bps |
| BAL | 0.788 | 0.413 | 42.01 bps |
| SHARP | 1.132 | 0.418 | 31.72 bps |

Small floating-point differences may occur across numerical-library versions. Structural conclusions should not.

## Research firewall

The final holdout is confirmatory.

A reproducible implementation must not:

- change finalist parameters after viewing 2025+;
- fit a post-holdout ensemble;
- add a beta hedge based on final-sample diagnostics;
- remove assets after final-sample inspection;
- redesign long/short legs from final attribution;
- reinterpret the original validation failure as a pass.

## Local project root

The public notebooks support a `CRYPTO_ALPHA_ROOT` environment variable for locating a full local rebuild tree.

Example:

```bash
export CRYPTO_ALPHA_ROOT="/path/to/crypto-alpha-research"
```

For lightweight reviewer mode, the repository will progressively move required public logic and artifacts under the public repo itself so that no private research tree is required.

## Current packaging status

The six public notebooks and small frozen artifacts are complete.

Repository engineering is still in progress. Shared `src/` code, tests, scripts, and curated figures are being separated from the original private research workspace.
