# Public Data

This directory intentionally contains **only small point-in-time universe metadata**.

Included:

- `universe/monthly_universe.csv` — monthly research-universe membership;
- `universe/research_symbols.csv` — union of symbols appearing in the research universe.

Not included:

- raw Binance bars;
- processed 4h or 1h market data;
- final-holdout caches;
- portfolio weight panels;
- execution caches;
- large intermediate research panels.

The exclusion is intentional: the GitHub repository is designed to be inspectable and reproducible without committing large exchange datasets.

See `../docs/reproducibility.md` for the rebuild policy.
