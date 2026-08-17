import json
from pathlib import Path

import numpy as np
import pandas as pd

from crypto_alpha.config import (
    FINALISTS,
    HOLDOUT_END,
    HOLDOUT_START,
    PRIMARY_COST_BPS,
)
from crypto_alpha.io import locate_repo_root


ROOT = locate_repo_root(Path(__file__).resolve())


def test_public_universe_invariants():
    path = ROOT / "data" / "universe" / "monthly_universe.csv"
    universe = pd.read_csv(path)
    universe["effective_month"] = pd.to_datetime(
        universe["effective_month"], utc=True
    )

    assert universe["effective_month"].nunique() == 76
    assert universe["symbol"].nunique() == 151
    assert (
        universe.groupby("effective_month")["symbol"]
        .nunique()
        .eq(25)
        .all()
    )


def test_frozen_finalist_definitions():
    path = ROOT / "results" / "tables" / "frozen_finalists.csv"
    frozen = pd.read_csv(path).set_index("finalist")

    assert set(frozen.index) == set(FINALISTS)

    for finalist, spec in FINALISTS.items():
        row = frozen.loc[finalist]
        assert row["mapping"] == spec["mapping"]
        assert row["formation"] == spec["formation"]
        assert row["holding"] == spec["holding"]
        assert row["cadence"] == spec["cadence"]


def test_final_holdout_protocol():
    path = ROOT / "results" / "tables" / "final_holdout_protocol.json"
    with open(path, "r", encoding="utf-8") as f:
        protocol = json.load(f)

    assert protocol["holdout_start"] == str(HOLDOUT_START)
    assert protocol["holdout_end_exclusive"] == str(HOLDOUT_END)
    assert float(protocol["primary_cost_bps"]) == PRIMARY_COST_BPS
    assert protocol["combined_portfolio"] is False


def test_original_validation_remains_failure():
    path = ROOT / "results" / "tables" / "failed_validation_summary.csv"
    failed = pd.read_csv(path)

    assert set(failed["candidate"]) == {
        "momentum_immediate",
        "momentum_delayed_1d",
    }
    assert (failed["mean_net_return_20bps"] < 0).all()
    assert (failed["net_sharpe_20bps"] < 0).all()
    assert (failed["break_even_bps"] < PRIMARY_COST_BPS).all()


def test_final_holdout_remains_three_of_three_pass():
    path = ROOT / "results" / "tables" / "final_holdout_metrics.csv"
    metrics = pd.read_csv(path).set_index("finalist")

    assert set(metrics.index) == set(FINALISTS)
    assert (metrics["mean_price_ic"] > 0).all()
    assert (metrics["gross_ann_return"] > 0).all()
    assert (metrics["break_even_cost_bps"] >= PRIMARY_COST_BPS).all()

    expected = {
        "ECON": {
            "gross_sharpe_ann": 0.333832,
            "net20_sharpe_ann": 0.099474,
            "break_even_cost_bps": 28.495171,
        },
        "BAL": {
            "gross_sharpe_ann": 0.788064,
            "net20_sharpe_ann": 0.412757,
            "break_even_cost_bps": 42.007634,
        },
        "SHARP": {
            "gross_sharpe_ann": 1.132380,
            "net20_sharpe_ann": 0.418355,
            "break_even_cost_bps": 31.723803,
        },
    }

    for finalist, values in expected.items():
        for metric, target in values.items():
            assert np.isclose(
                float(metrics.loc[finalist, metric]),
                target,
                atol=5e-6,
            )


def test_finalists_are_not_independent_alphas():
    path = ROOT / "results" / "tables" / "finalist_correlations_48h.csv"
    corr = pd.read_csv(path, index_col=0)

    assert corr.loc["ECON", "BAL"] > 0.80
    assert corr.loc["ECON", "SHARP"] > 0.80
    assert corr.loc["BAL", "SHARP"] > 0.90
