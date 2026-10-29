<p align="center">
<a href="https://pyfolio.ml4trading.io">
<img src="https://i.imgur.com/GD6TZ0D.png" width="35%">
</a>
</p>

![PyPI](https://img.shields.io/pypi/v/pyfolio-reloaded)
[![Tests](https://github.com/stefan-jansen/pyfolio-reloaded/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/stefan-jansen/pyfolio-reloaded/actions/workflows/unit_tests.yml)
[![PyPI](https://github.com/stefan-jansen/pyfolio-reloaded/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/stefan-jansen/pyfolio-reloaded/actions/workflows/build_wheels.yml)
[![Coverage Status](https://coveralls.io/repos/github/stefan-jansen/pyfolio-reloaded/badge.svg?branch=main)](https://coveralls.io/github/stefan-jansen/pyfolio-reloaded?branch=main)
![GitHub issues](https://img.shields.io/github/issues/stefan-jansen/pyfolio-reloaded)
![Twitter Follow](https://img.shields.io/twitter/follow/ml4trading?style=social)

pyfolio is a Python library for performance and risk analysis of financial portfolios.
It accepts returns, positions, and transactions from your own backtester, with optional
integration for [Zipline](https://zipline.ml4trading.io/).

## Maintenance and new development

Pyfolio Reloaded is in minimal maintenance. Further work is limited to critical bug fixes,
security issues, and essential compatibility updates.
All new feature development focuses on the current [ML4T libraries](https://www.ml4trading.io/libraries/),
including [ML4T Diagnostic](https://github.com/ml4t/diagnostic).
For new projects, we recommend evaluating Diagnostic through its
[migration guide](https://www.ml4trading.io/docs/diagnostic/user-guide/migration/#pyfolio-portfolio-and-performance-analysis),
which includes a runnable portfolio example and explains differences between the workflows.
See the [Diagnostic documentation](https://www.ml4trading.io/docs/diagnostic/) for its supported APIs.

## Trading Strategy Analysis with pyfolio

At the core of pyfolio are various tear sheets that combine various individual plots and summary statistics to
provide a comprehensive view of the performance of a trading algorithm.

Here's an example of a simple tear sheet analyzing a strategy executed with the Zipline backtesting engine:

### Performance Metrics

The tear sheet presents performance and risk metrics for the strategy separately during the backtest and out-of-sample periods:

<p align="center">
<a href="#">
<img src="https://i.imgur.com/bfwMeIV.png" width="50%">
</a>
</p>

### Performance Plots

In addition, it visualizes how several risk and return metrics behave over time:

<p align="center">
<a href="#">
<img src="https://i.imgur.com/5Hyuet3.png" width="85%">
</a>
</p>

## Installation

Pyfolio 0.10.0 and this source version support Python 3.11-3.15. Python 3.9 and 3.10
are retired. Existing release artifacts retain their
original Python requirements. See the [Python support schedule](https://devguide.python.org/versions/).

This source version supports pandas 3.0 and 3.1 on Python 3.11-3.15, alongside
the existing pandas 1.5/2.x combinations where supported by the interpreter.
Pandas 3.2 and later are not yet qualified.
Published 0.10.0 permits pandas 3.0 only on Python 3.15.

Pandas 3.1 requires NumPy 2.0.2 or newer on Python 3.11-3.13. The dependency
resolver applies its requirements alongside the Python-specific floors below.

When sharing an environment with Zipline, its dependency constraints also apply.
Zipline Reloaded 3.2.0 requires pandas below 3.0; use a compatible pandas 2.x
environment for that integration. Pyfolio itself does not require Zipline.

Python 3.14 requires pandas 2.3.3 or newer and NumPy 2.3.3 or newer. Python 3.15 requires
pandas 3.0.6 and NumPy 2.5.4 or newer; pandas 2.3.3 crashes during date-range
construction in the stable CPython 3.15 Linux qualification. The dependency markers
select the appropriate combination. Bottleneck currently builds from source on
Python 3.15, so that installation needs a C compiler.

To install a published Pyfolio release into a supported environment, run:

```bash
pip install pyfolio-reloaded
```

The Conda channel contains historical releases:

```bash
conda install -c ml4t pyfolio-reloaded
```

The frozen Conda 0.9.4 recipe and existing channel artifacts are preserved.
That recipe does not build this source version, and its publishing workflow is retired.

### Development

Clone this repository, then create an isolated environment and install the declared extras:

```bash
uv venv --python 3.11
uv pip install -e '.[test,docs,dev]'
uv run pre-commit install
```

## Usage

A good way to get started is to run the pyfolio examples in a
[Jupyter notebook](https://jupyter.org/). To do this, you first want to
start a Jupyter notebook server:

```bash
jupyter notebook
```

From the notebook list page, navigate to the pyfolio examples directory
and open a notebook. Execute the code in a notebook cell by clicking on it
and hitting Shift+Enter.


## Questions?

If you find a bug, feel free to [open an issue](https://github.com/stefan-jansen/pyfolio-reloaded/issues) in this repository.

You can also join our [community](https://exchange.ml4trading.io).

## Support

Please [open an issue](https://github.com/stefan-jansen/pyfolio-reloaded/issues/new) for support.

## Contributing

Read the [contribution guide](https://github.com/stefan-jansen/pyfolio-reloaded/blob/main/CONTRIBUTING.md)
before submitting an issue or pull request. This library accepts bug, security and compatibility fixes.

If you'd like to contribute, a great place to look is the [issues marked with help-wanted](https://github.com/stefan-jansen/pyfolio-reloaded/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22).

For a list of core developers and outside collaborators, see [the GitHub contributors list](https://github.com/stefan-jansen/pyfolio-reloaded/graphs/contributors).
