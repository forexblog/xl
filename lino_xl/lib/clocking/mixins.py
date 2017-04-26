# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines model mixins for this plugin."""


from django.db import models
from django.utils import timezone

from lino.api import dd, rt, _

from lino.mixins.periods import Monthly
from lino.modlib.printing.mixins import DirectPrintAction
from lino.core.roles import SiteUser
from .roles import Worker
from lino_xl.lib.tickets.roles import Triager

from .actions import StartTicketSession, EndTicketSession


class Workable(dd.Model):
    """Base class for things that workers can work on. 

    The model specified in :attr:`ticket_model
    <lino_xl.lib.clocking.Plugin.ticket_model>` must be a subclass of
    this.
    
    For example, in :ref:`noi` tickets are workable, or in
    :ref:`psico` partners are workable.

    """
    class Meta:
        abstract = True

    create_session_on_create = False

    start_session = StartTicketSession()
    end_session = EndTicketSession()

    def get_ticket(self):
        return self

    def is_workable_for(self, user):
        """Return True if the given user can start a working session on this
        object.

        """
        return True

    # def on_worked(self, session):
    #     """This is automatically called when a work session has been created
    #     or modified.

    #     """
    #     pass

    def save_new_instance(elem, ar):
        super(Workable, elem).save_new_instance(ar)

        if rt.settings.SITE.loading_from_dump:
            return
        me = ar.get_user()
        print elem.create_session_on_create
        if elem.create_session_on_create and me is not None and me.open_session_on_new_ticket:
            ses = rt.modules.clocking.Session(ticket=elem, user=me)
            ses.full_clean()
            ses.save()

