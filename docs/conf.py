# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default; values that are commented out
# serve to show the default.

extensions = []

from lino.sphinxcontrib import configure
configure(globals())

extensions += ['lino.sphinxcontrib.logo']


from atelier.sphinxconf import interproject
interproject.configure(globals())

from lino_xl import SETUP_INFO

# intersphinx_mapping = {}
# from importlib import import_module
# for n in 'atelier lino_book'.split():
#     m = import_module(n)
#     n = n.replace('_', "")
#     intersphinx_mapping[n] = (m.intersphinx_urls['docs'], None)

# General configuration
# ---------------------

# General information about the project.
project = "Lino XL docs"
copyright = '2014-2019 Rumma & Ko Ltd'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = SETUP_INFO['version']

# The short X.Y version.
version = '.'.join(release.split('.')[:2])


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.

exclude_patterns = [
    '.build/*',
    'shared/include/*',
]


# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = u"OpenTIM Developer's Reference"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'
#~ last_updated = True

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#~ html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# http://sphinx.pocoo.org/latest/config.html#confval-html_sidebars
html_sidebars = {
    '**': ['globaltoc.html', 'searchbox.html', 'links.html'],
}


# Additional templates that should be rendered to pages, maps page names to
# template names.
#~ html_additional_pages = {
    #~ '*': 'links.html',
#~ }


# If false, no module index is generated.
html_use_modindex = False

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
html_use_opensearch = ''
#~ html_use_opensearch = 'http://lino.saffre-rumma.net'

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'xl'


extlinks = {}
extlinks.update(ticket=('http://bugs.saffre-rumma.net/tickets/Ticket/%s', '#'))

