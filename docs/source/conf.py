# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from pyfolio import __version__ as version

extensions = [
    "sphinx.ext.autodoc",
    "numpydoc",
    "m2r2",
    "sphinx_markdown_tables",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

nbsphinx_execute = "never"

templates_path = ["_templates"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

master_doc = "index"

project = "pyfolio"
copyright = "2016, Quantopian, Inc."
author = "Quantopian, Inc."

release = version
language = "en"

exclude_patterns = []

highlight_language = "python"

pygments_style = "sphinx"

todo_include_todos = False

html_theme = "pydata_sphinx_theme"
html_title = "Pyfolio Reloaded"

html_theme_options = {
    "github_url": "https://github.com/stefan-jansen/pyfolio-reloaded",
    "twitter_url": "https://twitter.com/ml4trading",
    "external_links": [
        {"name": "ML for Trading", "url": "https://ml4trading.io"},
        {"name": "Community", "url": "https://exchange.ml4trading.io"},
    ],
    "use_edit_page_button": True,
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "stefan-jansen",
    "github_repo": "pyfolio-reloaded",
    "github_version": "main",
    "doc_path": "docs/source",
}

html_static_path = []

htmlhelp_basename = "Pyfoliodoc"

latex_elements = {}

latex_documents = [
    (
        master_doc,
        "Pyfolio.tex",
        "Pyfolio Documentation",
        "Quantopian, Inc.",
        "manual",
    )
]

man_pages = [(master_doc, "pyfolio", "Pyfolio Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "Pyfolio",
        "Pyfolio Documentation",
        author,
        "Pyfolio",
        "One line description of project.",
        "Miscellaneous",
    )
]
