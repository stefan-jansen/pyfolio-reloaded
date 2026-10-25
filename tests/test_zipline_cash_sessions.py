import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from pyfolio.utils import extract_rets_pos_txn_from_zipline


@pytest.mark.parametrize("traded", [False, True])
def test_zipline_extraction_retains_cash_sessions_and_empty_transactions(traded):
    dates = pd.date_range("2024-01-02", periods=3, tz="UTC")
    positions = [[], [], []]
    transactions = [[], [], []]
    cash = [1000.0, 1000.0, 1000.0]
    if traded:
        positions[1] = [{"sid": 1, "amount": 10, "last_sale_price": 10.0}]
        cash[1] = 900.0
        for day, amount in [(1, 10), (2, -10)]:
            transactions[day] = [
                {
                    "sid": 1,
                    "amount": amount,
                    "price": 10.0,
                    "commission": 0.0,
                    "order_id": f"order-{day}",
                    "dt": dates[day] + pd.Timedelta(hours=12),
                }
            ]
    result = pd.DataFrame(
        {
            "returns": [0.0, 0.0, 0.0],
            "positions": positions,
            "transactions": transactions,
            "ending_cash": cash,
            "portfolio_value": [1000.0, 1000.0, 1000.0],
        },
        index=dates,
    )
    returns, actual, fills = extract_rets_pos_txn_from_zipline(result)
    assert_series_equal(returns, result.returns)
    expected = pd.DataFrame({"cash": cash}, index=dates)
    if traded:
        expected.insert(0, 1, [0.0, 100.0, 0.0])
    expected.columns.name = "sid"
    assert_frame_equal(actual, expected, check_freq=False, check_names=False)
    assert actual.columns.name == "sid"
    assert_series_equal(
        actual.sum(axis=1), result.portfolio_value, check_names=False, check_freq=False
    )
    assert isinstance(fills.index, pd.DatetimeIndex)
    assert len(fills) == (2 if traded else 0)
    if traded:
        assert (fills.amount.abs() * fills.price).sum() == 200.0
