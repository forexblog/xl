# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""

from __future__ import unicode_literals

# import logging
# logger = logging.getLogger(__name__)


from lino.api import dd, _
from lino import mixins

# users = dd.resolve_app('users')


class Team(mixins.BabelNamed):

    class Meta:
        app_label = 'teams'
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        abstract = dd.is_abstract_model(__name__, 'Team')


class Teams(dd.Table):
    model = 'teams.Team'
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = 'name *'
    order_by = ["name"]

    insert_layout = """
    name
    """

    detail_layout = """
    id name
    teams.UsersByTeam
    """


dd.inject_field(
    'auth.User', 'team',
    dd.ForeignKey('teams.Team', blank=True, null=True))


from lino.modlib.auth.desktop import Users

class UsersByTeam(Users):
    master_key = 'team'
