import pandas as pd
import pytest

from pyfolio.round_trips import extract_round_trips, gen_round_trip_stats


def completed_trade(portfolio_value=None):
    dates = pd.to_datetime(["2025-01-02", "2025-01-03"])
    fills = pd.DataFrame(
        {"amount": [1, -1], "price": [100.0, 120.0], "symbol": ["A", "A"]},
        index=dates,
    )
    return extract_round_trips(fills, portfolio_value=portfolio_value)


def test_round_trip_stats_explain_missing_portfolio_nav():
    trades = completed_trade()
    assert trades.loc[0, "pnl"] == pytest.approx(20.0)
    assert trades.loc[0, "rt_returns"] == pytest.approx(0.20)
    with pytest.raises(ValueError, match="portfolio_value"):
        gen_round_trip_stats(trades)


def test_round_trip_stats_preserve_portfolio_relative_return_with_nav():
    nav = pd.Series(1000.0, index=pd.to_datetime(["2025-01-02", "2025-01-03"]))
    trades = completed_trade(nav)
    stats = gen_round_trip_stats(trades)
    assert stats["returns"].loc[
        "Avg returns all round_trips", "All trades"
    ] == pytest.approx(0.02)
    assert stats["symbols"].loc["Avg returns all round_trips", "A"] == pytest.approx(
        0.02
    )
