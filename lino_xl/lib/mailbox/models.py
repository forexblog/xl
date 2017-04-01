# -*- coding: UTF-8 -*-

"""Database models for `lino_xl.lib.mailbox`.

"""
import logging

logger = logging.getLogger(__name__)

from django_mailbox import models
from django.utils.translation import ugettext_lazy as _
import django.db.models
#
from lino.api import dd, rt

#
#

def preview(obj, ar):
    return obj.html or obj.text

def spam(obj):
    """Checks if the message is spam or not
    """
    if obj.subject.startswith("*****SPAM*****"):
        return True
    else:
        return False


dd.inject_field('django_mailbox.Message', 'preview',
                dd.VirtualField(dd.HtmlBox(_("Preview")), preview))

class MessagePointer(dd.Model):

    class Meta:
        app_label ='mailbox'
        verbose_name =_("Message pointer")
        verbose_name_plural =_("Message pointers")

    @dd.htmlbox(_("Preview"))
    def preview(self, ar):
        if ar is None:
            return ""
        return self.message.html or self.message.text

    message = dd.ForeignKey("django_mailbox.Message", related_name="pointer")

    ticket = dd.ForeignKey('tickets.Ticket')



from .ui import *

@dd.schedule_often(10)
def get_new_mail():
    for mb in rt.models.django_mailbox.Mailbox.objects.filter(active=True):
        mails = mb.get_new_mail()
        for mail in mails:
            if spam(mail):
                mail.spam = True
                mail.full_clean()
                mail.save()
        if mails:
            logger.info("got {} from mailbox: {}".format(mails,mb))


class DeleteSpam(dd.Action):

    show_in_bbar = True
    readonly = False
    # required_roles = dd.login_required(Worker)
    label = u"X"


    def run_from_ui(self, ar, **kw):
        spams = rt.models.django_mailbox.Message.objects.filter(spam = True)
        logger.info("Deleting Spam Messages [%s]"%spams)
        for obj in spams:
            obj.delete()
        ar.set_response(refresh=True)

dd.inject_action("django_mailbox.Message", DeleteSpam=DeleteSpam())
