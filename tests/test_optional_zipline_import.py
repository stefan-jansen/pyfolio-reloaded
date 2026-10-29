import os
from pathlib import Path
import subprocess
import sys


def test_optional_zipline_warning_does_not_break_strict_import_and_metrics(tmp_path):
    source = Path(__file__).resolve().parents[1] / "src"
    environment = {
        **os.environ,
        "PYTHONPATH": str(source),
        "MPLBACKEND": "Agg",
    }
    result = subprocess.run(
        [
            sys.executable,
            "-Werror::UserWarning",
            "-c",
            "import pandas as pd; import pyfolio; "
            "returns = pd.Series([0.01, -0.02, 0.03] * 20, "
            "index=pd.date_range('2025-01-01', periods=60)); "
            "stats = pyfolio.timeseries.perf_stats(returns); "
            "assert pd.notna(stats['Sharpe ratio'])",
        ],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
