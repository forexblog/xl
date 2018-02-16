# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from builtins import str
from django.conf import settings

from lino.api import dd, rt, _
from etgen.html import E

from lino.modlib.notify.mixins import ChangeObservable
from lino_xl.lib.contacts.mixins import ContactRelated

from .choicelists import ClientStates


class ClientBase(ChangeObservable):

    class Meta:
        abstract = True

    workflow_state_field = 'client_state'

    client_state = ClientStates.field()
        # default=ClientStates.newcomer.as_callable)

    @classmethod
    def setup_parameters(cls, fields):
        # note that ClientStates has a default_value
        fields.update(
            client_state=ClientStates.field(blank=True))
        fields.update(
            client_contact_type=dd.ForeignKey(
                'client.ClientContactType',
                blank=True,
                help_text=_("Only clients having a contact of that type")))
        fields.update(
            client_contact_company=dd.ForeignKey(
                'contacts.Company',
                blank=True, verbose_name=_("Client contact organization"),
                help_text=_("Only clients having a contact with that organization")))
        super(ClientBase, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(ClientBase, self).get_request_queryset(ar, **filter)

        pv = ar.param_values
        cct = pv.client_contact_type
        if cct:
            qs = qs.filter(clientcontact__type=cct)
        ccp = pv.client_contact_company
        if ccp:
            qs = qs.filter(clientcontact__company=ccp)
        if pv.client_state:
            qs = qs.filter(client_state=pv.client_state)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(ClientBase, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        if pv.client_state:
            yield str(pv.client_state)
        if pv.client_contact_type:
            yield str(pv.client_contact_type)
        if pv.client_contact_company:
            yield str(pv.client_contact_company)

@dd.python_2_unicode_compatible
class ClientContactBase(ContactRelated):

    class Meta:
        abstract = True
        
    type = dd.ForeignKey(
        'clients.ClientContactType', blank=True, null=True)

    @dd.chooser()
    def company_choices(self, type):
        qs = rt.modules.contacts.Companies.request().data_iterator
        if type is not None:
            qs = qs.filter(client_contact_type=type)
        return qs

    @dd.chooser()
    def contact_person_choices(self, company, type):
        if company:
            return self.contact_person_choices_queryset(company)
        qs = rt.modules.contacts.Persons.request().data_iterator
        if type is not None:
            qs = qs.filter(client_contact_type=type)
        return qs

    def __str__(self):
        return str(self.contact_person or self.company or self.type)


