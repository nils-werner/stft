#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = 'default'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.pngmath',
    'sphinxcontrib.napoleon',
    'sphinx.ext.autosummary',
    'numpydoc',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'stft'
copyright = '2014, International AudioLabs Erlangen'

version = '0.4.7'
release = version

exclude_patterns = ['_build', '**tests**', '**setup**', '**extern**',
                    '**data**']

pygments_style = 'sphinx'

html_static_path = ['_static']

htmlhelp_basename = 'stftdoc'

latex_elements = {
}

latex_documents = [
    ('index', 'stft.tex', 'stft Documentation',
     'International AudioLabs Erlangen', 'manual'),
]

man_pages = [
    ('index', 'stft', 'stft Documentation',
     ['International AudioLabs Erlangen'], 1)
]

texinfo_documents = [
    ('index', 'stft', 'stft Documentation',
     'International AudioLabs Erlangen', 'stft',
     'One line description of project.',
     'Miscellaneous'),
]
