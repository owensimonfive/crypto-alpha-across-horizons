import numpy as np
import pandas as pd

from crypto_alpha.metrics import (
    annualized_mean_return,
    annualized_sharpe,
    break_even_bps,
    compounded_return,
    net_of_costs,
    overlap_hac_lags,
    periods_per_year,
)


def test_24_7_annualization():
    assert np.isclose(periods_per_year(24), 365.25)
    assert np.isclose(periods_per_year(48), 365.25 / 2)


def test_cost_identity_and_break_even():
    gross = pd.Series([0.0020, 0.0010, -0.0005])
    turnover = pd.Series([0.50, 0.25, 0.25])

    be = break_even_bps(gross, turnover)
    net_at_be = net_of_costs(gross, turnover, be)

    assert np.isclose(net_at_be.sum(), 0.0, atol=1e-14)


def test_compounded_return():
    r = pd.Series([0.10, -0.05])
    expected = 1.10 * 0.95 - 1.0
    assert np.isclose(compounded_return(r), expected)


def test_annualized_sharpe_is_nan_for_constant_series():
    r = pd.Series([0.01, 0.01, 0.01])
    assert np.isnan(annualized_sharpe(r, 365.25))


def test_annualized_mean_return():
    r = pd.Series([0.01, -0.005, 0.0])
    assert np.isclose(
        annualized_mean_return(r, 100),
        r.mean() * 100,
    )


def test_overlap_hac_lags():
    assert overlap_hac_lags(6 * 7 * 24, 24) == 41
    assert overlap_hac_lags(8 * 7 * 24, 48) == 27
    assert overlap_hac_lags(8 * 7 * 24, 8) == 167
