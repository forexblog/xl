# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for this plugin.

"""

from lino.core.roles import UserRole

class BlogsReader(UserRole):
    """If the aplication defines AnonymousUser having this role, then all
    blog entries are publicly visible.

    """
    pass

