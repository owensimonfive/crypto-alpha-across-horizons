"""Portfolio construction and execution-accounting helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def score_to_entry_weights(
    score: pd.Series,
    mapping: str = "continuous_rank",
) -> pd.Series:
    """Convert one cross-section of scores into a gross-1, net-0 portfolio.

    Supported mappings mirror the final research:
    - continuous_rank
    - equal_weight_terciles
    """
    score = pd.Series(score, dtype=float)
    valid = score.dropna()
    out = pd.Series(0.0, index=score.index, dtype=float)

    if len(valid) < 3:
        return out

    if mapping == "continuous_rank":
        ranks = valid.rank(method="average", pct=True)
        raw = ranks - ranks.mean()

        pos = raw.clip(lower=0.0)
        neg = -raw.clip(upper=0.0)

        if pos.sum() <= 0 or neg.sum() <= 0:
            return out

        out.loc[valid.index] = (
            0.5 * pos / pos.sum()
            - 0.5 * neg / neg.sum()
        )

    elif mapping == "equal_weight_terciles":
        ranks = valid.rank(method="average", pct=True)
        long_names = ranks[ranks > 2.0 / 3.0].index
        short_names = ranks[ranks <= 1.0 / 3.0].index

        if len(long_names) == 0 or len(short_names) == 0:
            return out

        out.loc[long_names] = 0.5 / len(long_names)
        out.loc[short_names] = -0.5 / len(short_names)

    else:
        raise ValueError(f"Unknown mapping: {mapping}")

    return out


def full_l1_turnover(weights: pd.DataFrame) -> pd.Series:
    """Full-L1 target-weight turnover."""
    w = weights.fillna(0.0).astype(float)
    prior = w.shift(1).fillna(0.0)
    return (w - prior).abs().sum(axis=1)


def assert_neutral_weights(
    weights: pd.DataFrame,
    atol: float = 1e-10,
) -> None:
    """Raise if non-empty target rows are not gross-1 / net-0."""
    w = weights.fillna(0.0).astype(float)
    gross = w.abs().sum(axis=1)
    net = w.sum(axis=1)
    active = gross > atol
    if active.any():
        if not np.allclose(gross.loc[active], 1.0, atol=atol):
            raise AssertionError("Active portfolio rows are not gross-1")
        if not np.allclose(net.loc[active], 0.0, atol=atol):
            raise AssertionError("Active portfolio rows are not net-0")
