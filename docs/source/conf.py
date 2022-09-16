# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AirTrafficSim'
copyright = '2022, HKUST OCTAD Lab'
author = 'HKUST OCTAD Lab'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.napoleon',
    "myst_parser",
    # 'sphinx.ext.coverage',
    # "sphinx.ext.autosummary",
    'numpydoc',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']
html_title = "AirTrafficSim"
html_favicon = "images/OCTAD_logo.png"

autoclass_content = 'both'
autodoc_member_order = 'bysource'

numpydoc_class_members_toctree = False
# numpydoc_attributes_as_param_list = False