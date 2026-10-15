import numpy as np
import pandas as pd
import pytest

from pyfolio.timeseries import perf_stats


def test_performance_statistics_compute_sortino_with_supported_numpy():
    returns = pd.Series([0.01, -0.02, 0.03] * 10)
    result = perf_stats(returns)
    expected = (
        returns.mean() * np.sqrt(252) / np.sqrt(np.mean(np.minimum(returns, 0) ** 2))
    )
    assert result["Sortino ratio"] == pytest.approx(expected)
