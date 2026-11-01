import empyrical as ep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from pyfolio import plotting, tears, timeseries

matplotlib.use("Agg")


@pytest.mark.parametrize("start", ["2024-01-01", "2024-12-30"])
def test_initial_loss_table_uses_starting_capital_and_actual_recovery(start):
    dates = pd.bdate_range(start, periods=6)
    returns = pd.Series([-0.1, -0.1, 0.05, 0.05, 0.1, 0.02], index=dates)
    result = timeseries.gen_drawdown_table(returns, top=3)
    assert result.loc[0, "Net drawdown in %"] == pytest.approx(19)
    assert result.loc[0, "Net drawdown in %"] == pytest.approx(
        -100 * ep.max_drawdown(returns)
    )
    assert result.loc[0, "Peak date"] == dates[0]
    assert result.loc[0, "Valley date"] == dates[1]
    assert result.loc[0, "Recovery date"] == dates[5]
    assert result.loc[0, "Duration"] == 6
    assert result.iloc[1:].isna().all().all()


@pytest.mark.parametrize(
    "values,depth,valley,recovery",
    [
        ([-0.1], 10, 0, None),
        ([-0.1, -0.2, -0.3], 49.6, 2, None),
        ([-0.1, 0.05, -0.2, 0.01], 24.4, 2, None),
        ([np.nan, -0.1, np.nan, -0.1, 0.25], 19, 3, 4),
        ([-1.0, 0.1, 0.2], 100, 0, None),
    ],
)
def test_loss_table_keeps_unrecovered_and_missing_return_boundaries(
    values, depth, valley, recovery
):
    dates = pd.date_range("2024-12-31", periods=len(values), freq="D")
    returns = pd.Series(values, index=dates)
    result = timeseries.gen_drawdown_table(returns, top=3)
    assert result.loc[0, "Net drawdown in %"] == pytest.approx(depth)
    assert result.loc[0, "Valley date"] == dates[valley]
    assert result.loc[0, "Net drawdown in %"] == pytest.approx(
        -100 * ep.max_drawdown(returns)
    )
    if recovery is None:
        assert pd.isna(result.loc[0, "Recovery date"])
        assert pd.isna(result.loc[0, "Duration"])
    else:
        assert result.loc[0, "Recovery date"] == dates[recovery]
    assert result.iloc[1:].isna().all().all()


def test_separate_initial_and_later_drawdowns_are_ranked_without_duplicates():
    returns = pd.Series(
        [-0.1, 0.25, -0.5, 1.0, -0.2],
        index=pd.bdate_range("2024-01-01", periods=5),
    )
    result = timeseries.gen_drawdown_table(returns, top=5)
    np.testing.assert_allclose(
        result["Net drawdown in %"].dropna().astype(float), [50, 20, 10]
    )
    assert result.loc[2, "Recovery date"] == returns.index[1]
    assert pd.isna(result.loc[1, "Recovery date"])


@pytest.mark.parametrize("values", [[np.nan] * 3, [0.0] * 3, [0.1] * 3])
def test_no_decline_does_not_create_a_zero_depth_drawdown(values):
    returns = pd.Series(values, index=pd.bdate_range("2024-01-01", periods=3))
    assert timeseries.get_top_drawdowns(returns) == []
    assert timeseries.gen_drawdown_table(returns).isna().all().all()


def test_underwater_area_includes_the_first_loss_and_correct_valley():
    returns = pd.Series(
        [-0.1, -0.1, 0.05, 0.05, 0.1, 0.02],
        index=pd.bdate_range("2024-01-01", periods=6),
    )
    figure, axis = plt.subplots()
    try:
        plotting.plot_drawdown_underwater(returns, ax=axis)
        vertices = axis.collections[0].get_paths()[0].vertices
        assert vertices[:, 1].min() == pytest.approx(-19)
        first_x = vertices[:, 0].min()
        assert vertices[vertices[:, 0] == first_x, 1].min() == pytest.approx(-10)
    finally:
        plt.close(figure)


def test_returns_tear_sheet_underwater_matches_the_max_drawdown_statistic():
    returns = pd.Series(
        [-0.1, -0.1, 0.05, 0.05, 0.1, 0.02],
        index=pd.bdate_range("2024-01-01", periods=6),
    )
    figure = tears.create_returns_tear_sheet(returns, return_fig=True)
    try:
        axis = next(ax for ax in figure.axes if ax.get_title() == "Underwater plot")
        depth = axis.collections[0].get_paths()[0].vertices[:, 1].min()
        assert depth == pytest.approx(-19)
        assert depth == pytest.approx(
            100 * timeseries.perf_stats(returns)["Max drawdown"]
        )
    finally:
        plt.close(figure)
