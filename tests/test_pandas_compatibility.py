import warnings
from contextlib import nullcontext
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import numpy as np
import pandas as pd
import pytest

from pyfolio import perf_attrib, plotting, tears, utils


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_stats_preserve_numeric_values_and_display_percentages():
    returns = pd.Series(
        [0.01, -0.02, 0.03] * 10, pd.date_range("2023-01-01", periods=30)
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message="Setting an item of incompatible dtype"
        )
        stats = plotting.show_perf_stats(returns, return_df=True)
    assert isinstance(stats.loc["Sharpe ratio", "Backtest"], float)
    assert stats.loc["Cumulative returns", "Backtest"].endswith("%")


def test_intraday_first_day_preserves_capital_with_copy_on_write():
    dates = pd.date_range("2023-01-01", periods=2, tz="UTC")
    returns = pd.Series([0.0, 0.0], dates)
    positions = pd.DataFrame({"A": [100.0, 100.0], "cash": [900.0, 900.0]}, index=dates)
    transactions = pd.DataFrame(
        {"symbol": ["A"], "amount": [10.0], "price": [10.0]},
        index=[dates[0] + pd.Timedelta(hours=12)],
    )
    context = (
        pd.option_context("mode.copy_on_write", True)
        if int(pd.__version__.split(".")[0]) < 3
        else nullcontext()
    )
    with context:
        actual = utils.estimate_intraday(returns, positions, transactions)
    assert actual.loc[dates[0], "cash"] == 900.0
    assert actual.loc[dates[0], "A"] == 100.0


def test_live_cone_uses_last_in_sample_value_without_positional_fallback():
    returns = pd.Series(
        np.random.default_rng(42).normal(0.001, 0.01, 300),
        pd.bdate_range("2020-01-01", periods=300, tz="UTC"),
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message="Series.__getitem__ treating keys as positions"
        )
        ax = plotting.plot_rolling_returns(
            returns, live_start_date=returns.index[250], cone_std=(1, 2)
        )
    assert len(ax.collections) == 2
    ax.figure.canvas.draw()


@pytest.mark.parametrize("color", [None, "orange"])
def test_live_return_quantiles_preserve_points_and_requested_color(color):
    returns = pd.Series(
        np.random.default_rng(42).normal(0.001, 0.01, 100),
        pd.bdate_range("2020-01-01", periods=100),
    )
    with warnings.catch_warnings():
        warnings.filterwarnings("error", message="Ignoring `palette`")
        warnings.filterwarnings("error", message="set_ticklabels\\(\\) should only")
        kwargs = {} if color is None else {"color": color}
        ax = plotting.plot_return_quantiles(
            returns, live_start_date=returns.index[80], **kwargs
        )
        ax.figure.canvas.draw()
    assert [label.get_text() for label in ax.get_xticklabels()] == [
        "Daily",
        "Weekly",
        "Monthly",
    ]
    assert [len(collection.get_offsets()) for collection in ax.collections] == [
        20,
        5,
        2,
    ]
    expected_color = to_rgb("red" if color is None else color)
    for collection in ax.collections:
        assert np.allclose(collection.get_facecolors()[:, :3], expected_color)
    assert to_rgb(ax.get_legend().get_lines()[0].get_color()) == expected_color


def test_round_trip_notebook_probability_and_pnl_ticks_do_not_overlap():
    data = Path(__file__).parent / "test_data"
    returns = utils.to_series(
        utils.to_utc(
            pd.read_csv(data / "test_returns.csv.gz", index_col=0, parse_dates=True)
        )
    )
    positions = utils.to_utc(
        pd.read_csv(data / "test_pos.csv.gz", index_col=0, parse_dates=True)
    )
    transactions = utils.to_utc(
        pd.read_csv(data / "test_txn.csv.gz", index_col=0, parse_dates=True)
    )
    figure = tears.create_round_trip_tear_sheet(
        returns, positions, transactions, return_fig=True
    )
    figure.canvas.draw()
    selected = [
        axis
        for axis in figure.axes
        if axis.get_xlabel()
        in [
            "Probability of making a profitable decision",
            "PnL per round-trip trade in $",
        ]
    ]
    assert len(selected) == 2
    for axis in selected:
        lower, upper = axis.get_xlim()
        boxes = [
            label.get_window_extent(figure.canvas.get_renderer())
            for location, label in zip(axis.get_xticks(), axis.get_xticklabels())
            if lower <= location <= upper
        ]
        assert all(left.x1 <= right.x0 for left, right in zip(boxes, boxes[1:]))


@pytest.mark.parametrize("partitioned", [False, True])
def test_attribution_tear_sheet_formats_percentages_without_changing_returns(
    partitioned,
):
    data = Path(__file__).parent / "test_data"
    positions = pd.read_csv(data / "positions.csv", index_col=0, parse_dates=True)
    positions.columns = [int(c) if c != "cash" else c for c in positions.columns]
    returns = (
        pd.read_csv(
            data / "returns.csv", index_col=0, parse_dates=True, header=None
        ).squeeze()
        / 100
    )
    factors = (
        pd.read_csv(data / "factor_returns.csv", index_col=0, parse_dates=True) / 100
    )
    loadings = pd.read_csv(
        data / "factor_loadings.csv", index_col=[0, 1], parse_dates=[0]
    )
    names = {"materials": "basic_materials", "financials": "financial_services"}
    factors = factors.rename(columns=names)
    loadings = loadings.rename(columns=names)
    expected_returns = returns.copy()
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message="Setting an item of incompatible dtype"
        )
        figure = tears.create_perf_attrib_tear_sheet(
            returns,
            positions,
            factors,
            loadings,
            return_fig=True,
            **({} if partitioned else {"factor_partitions": None}),
        )
        figure.canvas.draw()
    assert len(figure.axes) == (5 if partitioned else 3)
    legends = [axis.get_legend() for axis in figure.axes[1:] if axis.get_legend()]
    assert len(legends) == 2
    for legend in legends:
        assert set(factors.columns) <= {text.get_text() for text in legend.get_texts()}
    pd.testing.assert_series_equal(returns, expected_returns)
    exposures, attribution = perf_attrib.perf_attrib(
        returns, positions, factors, loadings
    )
    np.testing.assert_allclose(exposures, 1)
    np.testing.assert_allclose(attribution.common_returns, expected_returns)
    np.testing.assert_allclose(attribution.specific_returns, 0, atol=1e-11)


def test_alpha_return_histogram_renders_its_patch_and_reference_line_legend():
    alpha_returns = pd.Series(np.linspace(-0.03, 0.03, 30))
    axis = perf_attrib.plot_alpha_returns(alpha_returns)
    axis.figure.canvas.draw()
    labels = {text.get_text() for text in axis.get_legend().get_texts()}
    assert "Multi-factor alpha" in labels
    assert "Zero" in labels
    assert any(label.startswith("Mean =") for label in labels)
    assert len(axis.patches) > 0
