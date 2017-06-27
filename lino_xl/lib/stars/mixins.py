# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from builtins import str
from django.conf import settings
from lino.api import dd, rt, _
from lino.utils.xmlgen.html import E
from lino.modlib.office.roles import OfficeUser
from lino.modlib.notify.mixins import ChangeObservable
from six import string_types


def get_favourite(obj, user):
    if user.authenticated:
        qs = rt.modules.stars.Star.for_obj(obj, user=user)
        if qs.count() == 0:
            return None
        return qs[0]


class StarObject(dd.Action):
    sort_index = 100
    # label = "*"
    label = u"☆"  # 2606
    help_text = _("Star this database object.")
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.login_required(OfficeUser)

    def get_action_permission(self, ar, obj, state):
        star = get_favourite(obj, ar.get_user())
        if star is not None:
            return False
        return super(StarObject, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        Star = rt.modules.stars.Star
        obj = ar.selected_rows[0]
        Star.create_star(obj, ar)
        ar.success(
            _("{0} is now starred.").format(obj), refresh_all=True)

    # def create_star(self, obj, ar):
    #     Star = rt.modules.stars.Star
    #     Star(owner=obj, user=ar.get_user()).save()

class FullStarObject(StarObject):

    label = u"✫"  #10031 u+272f ✫
    # 9956 U+26e4 ⛤
    # 10027 U+272b ✯
    # 10031 u+272f ✫
    help_text = _("Star this database object.")

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if user.authenticated:
            master_star_qs = rt.modules.stars.Star.for_obj(obj, user=user, master__isnull=True)
            child_star_qs = rt.modules.stars.Star.for_obj(obj, user=user)
            if not (master_star_qs.count() == 0 and child_star_qs.count()):
                return False
        else:
            return False
        return super(StarObject, self).get_action_permission(ar, obj, state) #Skip StarObject method

class UnstarObject(dd.Action):
    sort_index = 100
    # label = "-"
    label = u"★"  # 2605

    help_text = _("Unstar this database object.")
    show_in_workflow = True
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if user.authenticated:
            master_star_qs = rt.modules.stars.Star.for_obj(obj, user=user, master__isnull=True)
            if not (master_star_qs.count()):
                return False
        else:
            return False
        return super(UnstarObject, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        self.delete_star(obj, ar)
        ar.success(
            _("{0} is no longer starred.").format(obj), refresh_all=True)

    def delete_star(self, obj, ar):
        user = ar.get_user()
        # children_star_qs = rt.modules.stars.Star.for_master(obj, user=user)
        # star = get_favourite(obj, ar.get_user())
        # children_star_qs.delete()
        # ON cascade delete?
        master_star_qs = rt.modules.stars.Star.for_obj(obj, user=user, master__isnull=True)
        master_star_qs.delete()

class Starrable(ChangeObservable):

    class Meta(object):
        abstract = True

    child_starrables = []
    """
    A list of (model, master-key, related_field) tuples for child starrables"""


    if dd.is_installed("stars"):

        star_object = StarObject()
        full_star_object = FullStarObject()
        unstar_object = UnstarObject()

        def get_change_observers(self):
            for o in super(Starrable, self).get_change_observers():
                yield o
            for star in self.get_stars():
                yield (star.user, star.user.mail_mode)

        def get_stars(self):
            for star in rt.models.stars.Star.for_obj(self):
                yield star

        def get_children_starrable(self, ar):
            for model, fk, related in self.child_starrables:
                model = dd.resolve_model(model) if isinstance(model, string_types) else model
                for obj in model.objects.filter(**{fk: self}):
                    yield obj if related is None else getattr(obj, related)
