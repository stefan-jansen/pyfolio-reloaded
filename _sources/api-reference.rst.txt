.. _api-reference:

API
===

The pyfolio API is organized into various modules:

* Tear Sheets: :mod:`pyfolio.tears`
* Time Series Metrics: :mod:`pyfolio.timeseries`
* Plotting Functions: :mod:`pyfolio.plotting`
* Performance Attribution: :mod:`pyfolio.perf_attrib`
* Utilities: :mod:`pyfolio.utils`

Timestamp and annualization conventions
----------------------------------------

Pyfolio retains its historical date handling. Supply returns, positions and transactions
with consistent timestamp and timezone conventions. Transaction volume and turnover group
observations by normalized civil date; they do not look up exchange sessions. In an
overnight market, two executions in one exchange session can therefore fall into different
daily groups. Pyfolio does not infer the intended session or reconcile inconsistent labels.

The legacy tear-sheet APIs have no uniform ``calendar`` selector. They do not implement
the current ML4T convention in which explicit ``calendar=None`` disables calendar handling.
A continuous, 24/7 exchange schedule and calendar-free observation-based analysis are
different contracts. Exchange-session assignment belongs upstream of these legacy APIs;
retain execution timestamps when preparing data rather than treating an inferred daily
label as the execution instant.

Standard daily performance statistics use 252 observations per year. Some standalone
``pyfolio.timeseries`` wrappers accept a ``period`` argument; standalone Empyrical functions
also expose explicit ``annualization`` where supported. Those choices do not change every
statistic or panel in a Pyfolio tear sheet. In particular, weekend observations, irregular
timestamp spacing or an overnight exchange do not automatically select a different
annualization scale. Use a consistent declared return frequency and verify the conventions
of each calculation when a daily, 252-period report is unsuitable.

These conventions remain unchanged for compatibility. See the maintenance and migration
guidance on the :doc:`home page <index>` for the current ML4T libraries; evaluate
session-aware successor workflows against their documented inputs and qualification scope.

Tear Sheets
-----------

Pyfolio combines key portfolio metrics in thematic plots and summary tear sheets.

.. automodule:: pyfolio.tears
    :members:
    :undoc-members:
    :show-inheritance:

Time Series Metrics
-------------------

The module :mod:`pyfolio.timeseries` provides performance and risk metrics.

.. automodule:: pyfolio.timeseries
    :members:
    :undoc-members:
    :show-inheritance:

Performance Attribution:
------------------------

The module :mod:`pyfolio.perf_attrib` provides performance and risk metrics.

.. automodule:: pyfolio.perf_attrib
    :members:
    :undoc-members:
    :show-inheritance:

Plotting Functions
------------------

The module :mod:`pyfolio.plotting` facilitates the visualization of performance metrics.

.. automodule:: pyfolio.plotting
    :members:
    :undoc-members:
    :show-inheritance:

Utilities
---------

The module :mod:`pyfolio.utils` contains various helper functions, e.g. to format factor data into the requisite input format.

.. automodule:: pyfolio.utils
    :members:
    :undoc-members:
    :show-inheritance:
