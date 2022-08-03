import sys
from os.path import abspath
from pathlib import Path
from json import loads as json_loads


ROOT = Path(__file__).resolve().parent

sys.path.insert(0, abspath("."))

# -- General configuration ------------------------------------------------

project = "pptrees"
version = "1.1.6"
copyright = "2020, tdene"
author = "tdene"

autodoc_member_order = "bysource"

extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinxcontrib.bibtex",
    "sphinx_autodoc_typehints",
    "sphinx_click",
    "sphinx_markdown_tables",
]

bibtex_default_style = "plain"
bibtex_bibfiles = [str(ROOT / "refs.bib")]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

todo_include_todos = True

templates_path = ["_templates"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

master_doc = "index"

project = "Parallel prefix tree generation and exploration"
author = "Teodor-Dumitru Ene"
copyright = "Teodor-Dumitru Ene"

version = "1.1.6"
release = version  # The full version, including alpha/beta/rc tags.

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "build",
    "extra",
]

# reST settings
prologPath = "prolog.inc"
try:
    with open(prologPath, "r") as prologFile:
        rst_prolog = prologFile.read()
except Exception as ex:
    print("[ERROR:] While reading '{0!s}'.".format(prologPath))
    print(ex)
    rst_prolog = ""

# -- Options for HTML output ----------------------------------------------

myst_html_meta = {
    "description lang=en": "metadata description",
    "description lang=fr": "description des métadonnées",
    "keywords": "Sphinx, MyST",
    "property=og:locale": "en_US",
}

html_context = {}
ctx = ROOT / "context.json"
if ctx.is_file():
    html_context.update(json_loads(ctx.open("r").read()))

if (ROOT / "_theme").is_dir():
    html_theme_path = ["."]
    html_theme = "_theme"
    html_theme_options = {
        "logo_only": True,
        "home_breadcrumbs": True,
        "vcs_pageview_mode": "blob",
    }
else:
    html_theme = "sphinx_rtd_theme"

htmlhelp_basename = "pptrees_doc"

# -- Sphinx.Ext.InterSphinx -----------------------------------------------

intersphinx_mapping = {"python": ("https://docs.python.org/3.7/", None)}

# -- Sphinx.Ext.ExtLinks --------------------------------------------------
extlinks = {"wikipedia": ("https://en.wikipedia.org/wiki/%s", None)}
