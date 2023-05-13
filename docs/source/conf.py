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

# generate documentation from type hints
autodoc_typehints = 'description'
autoclass_content = 'both'

add_module_names = False

templates_path = ['_templates']
exclude_patterns = []

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'
# html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add the appropriate title to rst files
for rst_file_name in os.listdir(r'C:\Users\brand\Documents\ManimCS\docs\source'):
    if not rst_file_name.endswith('.rst') or rst_file_name == 'index.rst':
        continue

    content_lines: list[str] = []
    with open(rst_file_name) as rst_file:
        # rst_file.readlines() separates each line into a list BUT EACH LINE STILL HAS ``\n``
        content_lines = rst_file.read().splitlines()

    if rst_file_name == 'modules.rst':
        new_start: int = 0
        for line in content_lines:
            if line.strip() == '.. toctree::':
                break
            new_start += 1
        new_contents: str = '\n'.join(content_lines[new_start:])
        with open(rst_file_name, 'w') as rst_file:
            rst_file.write(new_contents)
        break

    proper_title: str = rst_file_name.split('.')[-2].capitalize()

    if content_lines[0] == proper_title:
        continue

    content_lines[0] = proper_title

    new_contents: str = '\n'.join(content_lines)

    # # new_contents: str = f'{proper_title}\n{title_underline}\n\n{contents}'

    with open(rst_file_name, 'w') as rst_file:
        rst_file.write(new_contents)
