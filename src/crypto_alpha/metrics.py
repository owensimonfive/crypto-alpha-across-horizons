"""Performance, cost, and inference utilities used across the research."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import statsmodels.api as sm


def periods_per_year(cadence_hours: float) -> float:
    """Annualization factor for a 24/7 market using 365.25 days."""
    if cadence_hours <= 0:
        raise ValueError("cadence_hours must be positive")
    return 365.25 * 24.0 / float(cadence_hours)


def annualized_mean_return(r, periods_per_year_: float) -> float:
    x = pd.Series(r).dropna().astype(float)
    if len(x) == 0:
        return np.nan
    return float(x.mean() * periods_per_year_)


def annualized_volatility(r, periods_per_year_: float) -> float:
    x = pd.Series(r).dropna().astype(float)
    if len(x) < 2:
        return np.nan
    return float(x.std(ddof=1) * np.sqrt(periods_per_year_))


def annualized_sharpe(r, periods_per_year_: float) -> float:
    x = pd.Series(r).dropna().astype(float)
    if len(x) < 2:
        return np.nan
    sigma = float(x.std(ddof=1))
    if not np.isfinite(sigma) or sigma <= 0:
        return np.nan
    return float(x.mean() / sigma * np.sqrt(periods_per_year_))


def compounded_return(r) -> float:
    x = pd.Series(r).dropna().astype(float)
    if len(x) == 0:
        return np.nan
    return float((1.0 + x).prod() - 1.0)


def max_drawdown(r) -> float:
    x = pd.Series(r).dropna().astype(float)
    if len(x) == 0:
        return np.nan
    wealth = (1.0 + x).cumprod()
    return float((wealth / wealth.cummax() - 1.0).min())


def net_of_costs(gross_return, turnover, cost_bps: float) -> pd.Series:
    """Apply cost_bps per unit of full-L1 turnover."""
    gross = pd.Series(gross_return, copy=False).astype(float)
    to = pd.Series(turnover, index=gross.index, copy=False).astype(float)
    return gross - float(cost_bps) * 1e-4 * to


def break_even_bps(gross_return, turnover) -> float:
    """Cost per unit turnover that drives arithmetic mean P&L to zero."""
    gross = pd.Series(gross_return).dropna().astype(float)
    to = pd.Series(turnover).reindex(gross.index).astype(float)
    valid = gross.notna() & to.notna()
    gross = gross.loc[valid]
    to = to.loc[valid]
    denom = float(to.sum())
    if denom <= 0:
        return np.nan
    return float(gross.sum() / denom * 1e4)


def overlap_hac_lags(holding_hours: float, cadence_hours: float) -> int:
    """Overlap-aware HAC lag used for finalist IC inference."""
    if holding_hours <= 0 or cadence_hours <= 0:
        raise ValueError("holding_hours and cadence_hours must be positive")
    return max(0, int(math.ceil(holding_hours / cadence_hours) - 1))


def hac_mean_tstat(x, maxlags: int) -> float:
    """HAC/Newey-West t-statistic for the mean of a time series."""
    values = pd.Series(x).dropna().astype(float)
    if len(values) < 20:
        return np.nan
    maxlags = int(min(maxlags, len(values) - 1))
    X = np.ones((len(values), 1), dtype=float)
    fit = sm.OLS(values.to_numpy(), X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": maxlags},
    )
    return float(fit.tvalues[0])


def historical_expected_shortfall(r, alpha: float = 0.05) -> tuple[float, int]:
    """Historical expected shortfall in the worst alpha fraction."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0, 1]")
    x = np.sort(pd.Series(r).dropna().astype(float).to_numpy())
    if len(x) == 0:
        return np.nan, 0
    n_tail = max(1, int(np.ceil(alpha * len(x))))
    return float(x[:n_tail].mean()), n_tail


def single_factor_hac_regression(
    strategy_return,
    factor_return,
    maxlags: int = 4,
) -> dict[str, float]:
    """HAC single-factor regression used in final market-exposure diagnostics."""
    aligned = pd.concat(
        [
            pd.Series(strategy_return).rename("strategy"),
            pd.Series(factor_return).rename("factor"),
        ],
        axis=1,
    ).dropna()

    if len(aligned) < 3:
        raise ValueError("Need at least three aligned observations")

    model = sm.OLS(
        aligned["strategy"],
        sm.add_constant(aligned["factor"]),
    ).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": min(int(maxlags), len(aligned) - 1)},
    )

    return {
        "n_blocks": int(len(aligned)),
        "correlation": float(aligned["strategy"].corr(aligned["factor"])),
        "alpha": float(model.params["const"]),
        "alpha_hac_t": float(model.tvalues["const"]),
        "beta": float(model.params["factor"]),
        "beta_hac_t": float(model.tvalues["factor"]),
        "r_squared": float(model.rsquared),
    }
