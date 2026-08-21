from unittest import TestCase
import pandas as pd
import pytest

from pyfolio.plotting import show_perf_stats


class TestPlotting(TestCase):
    def test_show_perf_stats_non_datetime_index_raises_type_error(self):
        returns = pd.Series([0.01, -0.02, 0.03])
        with pytest.raises(TypeError, match="returns.index must be a pd.DatetimeIndex"):
            show_perf_stats(returns)
