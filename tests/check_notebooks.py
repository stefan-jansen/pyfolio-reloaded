"""Execute the original offline portfolio notebooks against an installed package."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
import pandas as pd
import pyfolio


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    package = Path(pyfolio.__file__).resolve().parent
    assert package.is_relative_to(Path(sys.prefix).resolve()), package
    results = {
        "python": sys.version,
        "pandas": pd.__version__,
        "pyfolio": pyfolio.__version__,
        "module": str(package),
        "notebooks": [],
    }
    with tempfile.TemporaryDirectory(prefix="pyfolio-notebooks-") as temporary:
        scratch = Path(temporary)
        work = scratch / "examples"
        work.mkdir()
        shutil.copytree(
            Path(__file__).parent / "test_data", scratch / "tests" / "test_data"
        )
        for name in [
            "round_trip_tear_sheet_example",
            "sector_mappings_example",
            "slippage_example",
        ]:
            original = package / "examples" / f"{name}.ipynb"
            notebook = nbformat.read(original, as_version=4)
            code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
            notebook.cells.insert(
                0,
                nbformat.v4.new_code_cell(
                    "import sys, pyfolio\n"
                    f"assert sys.prefix == {sys.prefix!r}\n"
                    f"assert pyfolio.__file__ == {pyfolio.__file__!r}\n"
                ),
            )
            client = NotebookClient(notebook, timeout=300, kernel_name="python3")
            client.km = client.create_kernel_manager()
            client.km.transport = "ipc"
            client.execute(cwd=str(work))
            images = [
                result["data"]["image/png"]
                for cell in notebook.cells
                for result in cell.get("outputs", [])
                if "image/png" in result.get("data", {})
            ]
            assert images, f"{name} generated no portfolio figures"
            (output / f"{name}.png").write_bytes(base64.b64decode(images[-1]))
            results["notebooks"].append(
                {
                    "name": name,
                    "source_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
                    "original_code_cells": code_cells,
                    "rendered_figures": len(images),
                    "result": "pass",
                }
            )
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
