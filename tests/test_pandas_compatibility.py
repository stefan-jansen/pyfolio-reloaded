import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from pyfolio import plotting, utils


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_stats_preserve_numeric_values_and_display_percentages():
    returns = pd.Series(
        [0.01, -0.02, 0.03] * 10, pd.date_range("2023-01-01", periods=30)
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message="Setting an item of incompatible dtype"
        )
        stats = plotting.show_perf_stats(returns, return_df=True)
    assert isinstance(stats.loc["Sharpe ratio", "Backtest"], float)
    assert stats.loc["Cumulative returns", "Backtest"].endswith("%")


def test_intraday_first_day_preserves_capital_with_copy_on_write():
    dates = pd.date_range("2023-01-01", periods=2, tz="UTC")
    returns = pd.Series([0.0, 0.0], dates)
    positions = pd.DataFrame({"A": [100.0, 100.0], "cash": [900.0, 900.0]}, index=dates)
    transactions = pd.DataFrame(
        {"symbol": ["A"], "amount": [10.0], "price": [10.0]},
        index=[dates[0] + pd.Timedelta(hours=12)],
    )
    with pd.option_context("mode.copy_on_write", True):
        actual = utils.estimate_intraday(returns, positions, transactions)
    assert actual.loc[dates[0], "cash"] == 900.0
    assert actual.loc[dates[0], "A"] == 100.0


def test_live_cone_uses_last_in_sample_value_without_positional_fallback():
    returns = pd.Series(
        np.random.default_rng(42).normal(0.001, 0.01, 300),
        pd.bdate_range("2020-01-01", periods=300, tz="UTC"),
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message="Series.__getitem__ treating keys as positions"
        )
        ax = plotting.plot_rolling_returns(
            returns, live_start_date=returns.index[250], cone_std=(1, 2)
        )
    assert len(ax.collections) == 2
    ax.figure.canvas.draw()
