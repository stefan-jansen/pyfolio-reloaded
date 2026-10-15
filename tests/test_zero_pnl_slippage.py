import pandas as pd
from pandas.testing import assert_series_equal

from pyfolio import txn


def test_zero_pnl_days_preserve_returns_and_charge_actual_slippage():
    dates = pd.date_range("2020-01-01", periods=4, tz="UTC")
    returns = pd.Series([0.0, 0.0, 0.02, -0.01], dates, name="strategy")
    positions = pd.DataFrame({"A": 100.0, "cash": 900.0}, index=dates)
    transactions = pd.DataFrame(
        {"symbol": ["A"] * 3, "amount": [10.0] * 3, "price": [10.0] * 3},
        index=dates[1:],
    )
    result = txn.adjust_returns_for_slippage(returns, positions, transactions, 10)
    assert_series_equal(
        result, pd.Series([0.0, -0.0001, 0.0199, -0.0101], dates), check_names=False
    )
    assert_series_equal(
        returns, pd.Series([0.0, 0.0, 0.02, -0.01], dates, name="strategy")
    )
