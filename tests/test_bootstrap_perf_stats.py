import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from pyfolio import plotting, tears, timeseries


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_show_perf_stats_bootstrap_preserves_summary_columns_and_values():
    dates = pd.date_range("2024-01-02", periods=60, freq="B", tz="UTC")
    returns = pd.Series([0.002, -0.001, 0.003] * 20, index=dates)

    np.random.seed(0)
    expected = timeseries.perf_stats_bootstrap(returns)

    np.random.seed(0)
    stats = plotting.show_perf_stats(returns, bootstrap=True, return_df=True)

    assert list(stats.columns) == ["mean", "median", "5%", "95%"]
    assert not stats.isna().any().any()
    pct_stats = [stat for stat in plotting.STAT_FUNCS_PCT if stat in stats.index]
    assert pct_stats
    for col in stats.columns:
        for stat in pct_stats:
            assert isinstance(stats.loc[stat, col], str)
            assert stats.loc[stat, col].endswith("%")
            assert stats.loc[stat, col] != "nan%"
        assert isinstance(stats.loc["Sharpe ratio", col], float)
        assert np.isfinite(stats.loc["Sharpe ratio", col])
        assert stats.loc["Sharpe ratio", col] == pytest.approx(
            expected.loc["Sharpe ratio", col]
        )


def test_show_perf_stats_bootstrap_with_live_start_and_tear_sheet():
    dates = pd.date_range("2024-01-02", periods=60, freq="B", tz="UTC")
    returns = pd.Series([0.002, -0.001, 0.003] * 20, index=dates)

    np.random.seed(0)
    stats = plotting.show_perf_stats(
        returns,
        live_start_date=dates[30],
        bootstrap=True,
        return_df=True,
    )

    assert isinstance(stats.columns, pd.MultiIndex)
    assert list(stats.columns.levels[0]) == ["In-sample", "Out-of-sample", "All"]
    assert not stats.isna().any().any()

    np.random.seed(0)
    tears.create_returns_tear_sheet(returns, benchmark_rets=returns, bootstrap=True)
