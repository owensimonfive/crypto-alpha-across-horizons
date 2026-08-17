import numpy as np
import pandas as pd

from crypto_alpha.portfolio import (
    assert_neutral_weights,
    full_l1_turnover,
    score_to_entry_weights,
)


def test_continuous_rank_weights_are_neutral():
    scores = pd.Series(
        {"A": -2.0, "B": -1.0, "C": 1.0, "D": 2.0}
    )
    w = score_to_entry_weights(scores, "continuous_rank")

    assert np.isclose(w.abs().sum(), 1.0)
    assert np.isclose(w.sum(), 0.0)


def test_tercile_weights_are_neutral():
    scores = pd.Series(
        {
            "A": -3.0,
            "B": -2.0,
            "C": -1.0,
            "D": 1.0,
            "E": 2.0,
            "F": 3.0,
        }
    )
    w = score_to_entry_weights(scores, "equal_weight_terciles")

    assert np.isclose(w.abs().sum(), 1.0)
    assert np.isclose(w.sum(), 0.0)


def test_full_l1_turnover():
    weights = pd.DataFrame(
        [
            [0.5, -0.5],
            [0.25, -0.25],
        ],
        columns=["A", "B"],
    )
    turnover = full_l1_turnover(weights)

    assert np.isclose(turnover.iloc[0], 1.0)
    assert np.isclose(turnover.iloc[1], 0.5)


def test_weight_assertion():
    weights = pd.DataFrame(
        [
            [0.5, -0.5, 0.0, 0.0],
            [0.25, -0.25, 0.25, -0.25],
        ],
        columns=["A", "B", "C", "D"],
    )

    assert_neutral_weights(weights)
