# Contributing to Pyfolio Reloaded

Follow the [shared ML4T contribution policy](https://github.com/ml4t/ecosystem/blob/main/CONTRIBUTING.md).
Pyfolio Reloaded accepts bug, security and compatibility fixes. Propose new features in the
[current ML4T libraries](https://github.com/ml4t/ecosystem).

Search this repository's issues before opening one. Describe one problem per issue and address
it in one focused PR with a closing reference. Automated dependency updates and administrative
metadata changes do not require a separate issue. Keep unrelated repairs and formatting separate.

For a bug fix, provide a regression through the affected public API or user workflow. Record the
base and fix revisions, environment, commands and results: the regression must fail because of
the defect on the base and pass with the fix. Correct verified defects even when numerical
results change. Agree changes to intended definitions, annualization, sign conventions or
defaults in the owning issue and document their compatibility impact. Existing output alone
is not evidence of correctness. Documentation changes need documentation checks, not artificial
regression tests.

Use the native checks in the [test workflow](https://github.com/stefan-jansen/pyfolio-reloaded/blob/main/.github/workflows/unit_tests.yml)
and [tox configuration](https://github.com/stefan-jansen/pyfolio-reloaded/blob/main/pyproject.toml).
For documentation, install the `docs` extra and Pandoc, then run
`uv run --extra docs make -C docs html SPHINXOPTS="-W --keep-going"`.
The static build preserves notebook outputs; it does not verify notebook execution.
Report any checks you could not run.

State whether you used AI tools and which parts they helped produce. Review and test your
submission yourself, and be able to explain its code, evidence and responses to review questions.
Wait for feedback on your first focused contribution before opening a large series of similar PRs.
Maintainers may request focused replacements for bundled submissions.

Report suspected vulnerabilities through the [shared security process](https://github.com/ml4t/ecosystem/blob/main/SECURITY.md).
For other questions, use this repository's issues or the [community forum](https://exchange.ml4trading.io).
