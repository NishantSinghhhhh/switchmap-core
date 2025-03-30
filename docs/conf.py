# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../switchmap'))  # Adjust to your module path

project = 'Switchmap-NG'
extensions = [
    'sphinx.ext.autodoc',    # Automatically extract docs from docstrings
    'sphinx.ext.napoleon',   # Support for Google or NumPy style docstrings
    'sphinx.ext.viewcode',   # Add links to source code
]

# Optionally, specify a theme
html_theme = 'alabaster'
