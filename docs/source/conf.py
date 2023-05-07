# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import annotations

import os
import sys
from pprint import pprint
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))

pprint(sys.path)

project = 'Code Curation'
copyright = '2023, Brandon Hubacher'
author = 'Brandon Hubacher'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxcontrib.apidoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinx_copybutton',
    'sphinxcontrib.programoutput',
    # 'sphinx.ext.intersphinx',
]

# autoclass_content = 'both'

add_module_names = False

templates_path = ['_templates']
exclude_patterns = []

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'
html_static_path = ['_static']
