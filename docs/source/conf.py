# flake8: noqa

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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os
import sys
import sphinx_rtd_theme 
sys.path.insert(0, os.path.abspath('../..'))
# -- Project information -----------------------------------------------------

project = 'JBrowse Jupyter'
copyright = '2021, Teresa De Jesus Martinez, JBrowse Team'
author = 'Teresa De Jesus Martinez, JBrowse Team'

# The full version, including alpha/beta/rc tags
release = '1.2.5'


# -- General configuration ---------------------------------------------------
# source_suffix = {
#     '.rst': 'restructuredtext',
#     '.md': 'markdown',
# }
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
#     'sphinx.ext.autodoc',
#     'sphinx.ext.napoleon',
#     'sphinx_rtd_theme',
#     'recommonmark',
#     'sphinx_markdown_tables',
#     'nbsphinx'
# ]
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', '_static']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinx_rtd_theme'
# pygments_style = 'default'
html_theme = "sphinx_rtd_theme"

html_title = "JBrowse Jupyter"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
suppress_warnings = ["myst.header"]
# html_logo = "_static/color_logomark.png"
# html_theme_options = {
#     'logo_only': True,
#     'display_version': True,
#     'prev_next_buttons_location': 'bottom',
#     'style_external_links': True,
#     # Toc options
#     'collapse_navigation': False,
#     'sticky_navigation': False,
#     'navigation_depth': 3,
#     'includehidden': True,
#     'titles_only': False
# }
add_module_names = False
