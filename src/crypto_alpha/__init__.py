"""Reusable utilities for the Crypto Alpha Across Horizons research package."""

from .config import FINALISTS, HOLDOUT_END, HOLDOUT_START, PRIMARY_COST_BPS
from .metrics import (
    annualized_mean_return,
    annualized_sharpe,
    annualized_volatility,
    break_even_bps,
    compounded_return,
    hac_mean_tstat,
    max_drawdown,
    net_of_costs,
)

__all__ = [
    "FINALISTS",
    "HOLDOUT_START",
    "HOLDOUT_END",
    "PRIMARY_COST_BPS",
    "annualized_mean_return",
    "annualized_sharpe",
    "annualized_volatility",
    "break_even_bps",
    "compounded_return",
    "hac_mean_tstat",
    "max_drawdown",
    "net_of_costs",
]
