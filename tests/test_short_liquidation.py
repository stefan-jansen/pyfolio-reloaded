import pandas as pd
import pytest

from pyfolio import capacity


@pytest.mark.parametrize("size", [100.0, -100.0])
def test_capacity_screen_reports_positive_liquidation_days_for_either_side(size):
    dates = pd.date_range("2020-01-01", periods=3)
    positions = pd.DataFrame({"A": size, "cash": 1000.0 - size}, index=dates)
    market = pd.DataFrame(
        {"A": [10.0, 100.0] * 3},
        index=pd.MultiIndex.from_product(
            [dates, ["price", "volume"]], names=["dt", "market_data"]
        ),
    )
    result = capacity.get_max_days_to_liquidate_by_ticker(
        positions,
        market,
        max_bar_consumption=0.1,
        capital_base=1000,
        mean_volume_window=1,
    )
    assert result.loc["A", "days_to_liquidate"] == pytest.approx(1.0)
    assert result.loc["A", "pos_alloc_pct"] == pytest.approx(size / 10)
    assert "A" in result[result.days_to_liquidate > 0.5].index
