import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pyfolio import perf_attrib


def test_cash_only_attribution_raises_domain_error_without_mutating_inputs():
    dates = pd.date_range("2020-01-01", periods=2)
    returns = pd.Series(0.0, dates)
    positions = pd.DataFrame({"cash": 100.0}, index=dates)
    factors = pd.DataFrame({"factor": [0.01, -0.01]}, index=dates)
    loadings = pd.DataFrame(
        {"factor": [1.0, 1.0]},
        index=pd.MultiIndex.from_product([dates, ["A"]], names=["dt", "ticker"]),
    )
    originals = [x.copy(deep=True) for x in (positions, factors, loadings)]
    with pytest.raises(ValueError, match="No factor loadings"):
        perf_attrib.perf_attrib(returns, positions, factors, loadings)
    for actual, expected in zip((positions, factors, loadings), originals):
        assert_frame_equal(actual, expected)
