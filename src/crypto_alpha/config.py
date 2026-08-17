"""Frozen research constants.

These values are part of the final research protocol. Repository refactoring must
not silently change them.
"""

from __future__ import annotations

import pandas as pd

PRIMARY_COST_BPS = 20.0

HOLDOUT_START = pd.Timestamp("2025-01-01 00:00:00", tz="UTC")
HOLDOUT_END = pd.Timestamp("2026-08-01 00:00:00", tz="UTC")

FINALISTS = {
    "ECON": {
        "philosophy": "Economic resilience",
        "mapping": "continuous_rank",
        "formation": "2w",
        "holding": "6w",
        "holding_hours": 6 * 7 * 24,
        "cadence": "24h",
        "cadence_hours": 24,
    },
    "BAL": {
        "philosophy": "Balanced",
        "mapping": "equal_weight_terciles",
        "formation": "3d",
        "holding": "8w",
        "holding_hours": 8 * 7 * 24,
        "cadence": "48h",
        "cadence_hours": 48,
    },
    "SHARP": {
        "philosophy": "Higher Sharpe",
        "mapping": "equal_weight_terciles",
        "formation": "1d",
        "holding": "8w",
        "holding_hours": 8 * 7 * 24,
        "cadence": "8h",
        "cadence_hours": 8,
    },
}

SURVIVAL_RULE = {
    "mean_continuation_ic_gt": 0.0,
    "gross_ann_return_gt": 0.0,
    "break_even_cost_bps_ge": PRIMARY_COST_BPS,
}
