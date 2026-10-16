import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from pyfolio import plotting, tears


@pytest.mark.parametrize("timezone", [None, "UTC", "America/New_York"])
def test_returns_tear_sheet_accepts_live_start_in_supported_index_timezones(timezone):
    dates = pd.bdate_range("2020-01-01", periods=300, tz=timezone)
    returns = pd.Series(np.random.default_rng(42).normal(0.001, 0.01, 300), dates)
    try:
        figure = tears.create_returns_tear_sheet(
            returns, live_start_date="2020-10-01", return_fig=True
        )
        figure.canvas.draw()
        assert figure.axes
    finally:
        plt.close("all")


@pytest.mark.parametrize("timezone", [None, "UTC", "America/New_York"])
def test_aware_live_start_keeps_utc_instant_across_dst(timezone):
    dates = pd.to_datetime(
        [
            "2020-03-08T04:00Z",
            "2020-03-08T05:00Z",
            "2020-03-08T07:00Z",
            "2020-03-08T08:00Z",
        ]
    )
    dates = dates.tz_localize(None) if timezone is None else dates.tz_convert(timezone)
    returns = pd.Series([0.01, 0.0, -0.01, 0.02], dates)
    stats = plotting.show_perf_stats(
        returns,
        live_start_date=pd.Timestamp("2020-03-08 03:00", tz="America/New_York"),
        return_df=True,
    )
    assert stats.loc["Cumulative returns", "In-sample"] == "1.0%"
    assert stats.loc["Cumulative returns", "Out-of-sample"] == "0.98%"
