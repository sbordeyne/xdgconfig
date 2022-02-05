# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys
import re
import pathlib

import sphinx_rtd_theme

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

# -- Project information -----------------------------------------------------

project = 'xdgconfig'
copyright = '2021, Dogeek'
author = 'Dogeek'

# The full version, including alpha/beta/rc tags
with open(pathlib.Path(__file__).parent.parent.parent / 'pyproject.toml') as f:
    release = re.search(
        r'^ *version ?= ?"(?P<version>.+?)"$',
        f.read(), flags=re.DOTALL | re.MULTILINE,
    )

release = release.groupdict().get('version', '1.0.0')

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'recommonmark',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'

autosummary_generate = True
autodoc_mock_imports = ['xdgconfig']


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__" or name.startswith('_'):
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
