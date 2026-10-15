import numpy as np
import pandas as pd
import pytest

from pyfolio.timeseries import sortino_ratio


@pytest.mark.parametrize(
    "period,factor", [("daily", 252), ("weekly", 52), ("monthly", 12)]
)
def test_sortino_annualizes_using_the_requested_observation_period(period, factor):
    returns = pd.Series([0.02, -0.01, 0.03, 0.01, -0.02] * 6)
    required_return = 0.001
    adjusted = returns - required_return
    expected = (
        adjusted.mean()
        * np.sqrt(factor)
        / np.sqrt(np.mean(np.minimum(adjusted, 0) ** 2))
    )
    assert sortino_ratio(returns, required_return, period) == pytest.approx(expected)
