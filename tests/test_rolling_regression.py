import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from pyfolio.timeseries import rolling_regression


def test_fits_when_each_factor_is_within_missing_data_threshold():
    dates = pd.bdate_range("2020-01-01", periods=12)
    factors = pd.DataFrame(
        np.random.default_rng(0).normal(size=(12, 2)),
        index=dates,
        columns=["market", "size"],
    )
    returns = 0.5 * factors.market + 0.25 * factors["size"]
    factors.iloc[0, 0] = np.nan
    factors.iloc[1, 1] = np.nan

    result = rolling_regression(returns, factors, rolling_window=9, nan_threshold=0.1)

    assert_allclose(
        result.loc[dates[9], ["market", "size"]].to_numpy(dtype=float), [0.5, 0.25]
    )
    assert_allclose(result.loc[dates[9], "alpha"], 0.0, atol=1e-12)


def test_skips_when_one_factor_exceeds_missing_data_threshold():
    dates = pd.bdate_range("2020-01-01", periods=12)
    factors = pd.DataFrame(
        np.random.default_rng(0).normal(size=(12, 2)),
        index=dates,
        columns=["market", "size"],
    )
    returns = 0.5 * factors.market + 0.25 * factors["size"]
    factors.iloc[:6, 1] = np.nan

    result = rolling_regression(returns, factors, rolling_window=9, nan_threshold=0.1)

    assert result.loc[dates[9]].isna().all()


def test_skips_when_aligned_factors_have_no_joint_observations():
    dates = pd.bdate_range("2020-01-01", periods=8)
    factors = pd.concat(
        [
            pd.Series(0.01, index=dates[::2], name="market"),
            pd.Series(0.02, index=dates[1::2], name="size"),
        ],
        axis=1,
    ).sort_index()
    returns = pd.Series(0.01, index=dates)

    result = rolling_regression(returns, factors, rolling_window=3, nan_threshold=0.5)

    assert result.isna().all().all()
