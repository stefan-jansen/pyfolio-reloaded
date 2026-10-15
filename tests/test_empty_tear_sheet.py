import pandas as pd
import pytest

from pyfolio import tears


@pytest.mark.parametrize(
    "create", [tears.create_returns_tear_sheet, tears.create_full_tear_sheet]
)
def test_empty_download_cannot_produce_a_misleading_tear_sheet(create):
    returns = pd.Series(dtype=float, index=pd.DatetimeIndex([]))
    with pytest.raises(
        ValueError, match="returns must contain at least one observation"
    ):
        create(returns)
