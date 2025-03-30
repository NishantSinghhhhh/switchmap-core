# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../switchmap'))  

project = 'Switchmap-NG'
extensions = [
    'sphinx.ext.autodoc',    # Automatically extract docs from docstrings
    'sphinx.ext.napoleon',   # Support for Google or NumPy style docstrings
    'sphinx.ext.viewcode',   # Add links to source code
]


html_theme = 'alabaster'
