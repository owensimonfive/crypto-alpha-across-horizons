"""Cross-sectional signal helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def centered_rank(row: pd.Series) -> pd.Series:
    """Cross-sectional percentile rank centered on zero."""
    valid = row.dropna()
    out = pd.Series(np.nan, index=row.index, dtype=float)
    if len(valid) < 2:
        return out
    ranks = valid.rank(method="average", pct=True)
    out.loc[valid.index] = ranks - ranks.mean()
    return out


def rowwise_spearman(signal: pd.DataFrame, forward_return: pd.DataFrame) -> pd.Series:
    """Timestamp-by-timestamp cross-sectional Spearman IC."""
    common_index = signal.index.intersection(forward_return.index)
    common_columns = signal.columns.intersection(forward_return.columns)

    out = {}
    for ts in common_index:
        x = signal.loc[ts, common_columns]
        y = forward_return.loc[ts, common_columns]
        valid = x.notna() & y.notna()
        if int(valid.sum()) < 3:
            out[ts] = np.nan
        else:
            out[ts] = float(x.loc[valid].corr(y.loc[valid], method="spearman"))
    return pd.Series(out, name="price_ic").sort_index()


def exact_endpoint_return(
    close: pd.DataFrame,
    start_times: pd.DatetimeIndex,
    horizon: pd.Timedelta,
) -> pd.DataFrame:
    """Exact elapsed close-to-close return from t to t+horizon.

    Both endpoints must exist. Missing timestamps are not forward-filled.
    """
    start_times = pd.DatetimeIndex(start_times)
    end_times = start_times + horizon

    start = close.reindex(start_times)
    end = close.reindex(end_times)
    end.index = start_times

    return end / start - 1.0
