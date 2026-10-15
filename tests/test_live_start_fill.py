import pandas as pd

from pyfolio import plotting


def test_live_start_fill_belongs_to_out_of_sample_exactly_once():
    dates = pd.date_range("2020-01-01", periods=4, tz="UTC")
    returns = pd.Series([0.01, -0.01, 0.0, 0.01], dates)
    positions = pd.DataFrame({"A": 100.0, "cash": 0.0}, index=dates)
    transactions = pd.DataFrame(
        {"symbol": ["A", "A"], "amount": [10.0, 10.0], "price": [10.0, 10.0]},
        index=dates[:2],
    )
    stats = plotting.show_perf_stats(
        returns,
        positions=positions,
        transactions=transactions,
        live_start_date=dates[1],
        return_df=True,
    )
    assert stats.loc["Daily turnover", "In-sample"] == "200.0%"
    assert stats.loc["Daily turnover", "Out-of-sample"] == "66.667%"
    assert stats.loc["Daily turnover", "All"] == "75.0%"
