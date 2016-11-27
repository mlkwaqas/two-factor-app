from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

AUTHY_STATUSES = (
    'unverified', ''
    'onetouch',
    'sms',
    'token',
    'approved',
    'denied'
)

AUTHY_STATUSES = (
    ("unverified", _("unverified")),
    ("onetouch", _("onetouch")),
    ("sms", _("sms")),
    ("token", _("token")),
    ("approved", _("approved")),
    ("denied", _("denied")),
)


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    authy_status = models.CharField(max_length=10, choices=AUTHY_STATUSES, default='unverified')
    phone_number = models.CharField(max_length=100, null=True)
    country_code = models.IntegerField(null=True)
    authy_id = models.IntegerField(null=True)

    def __unicode__(self):
        return u"{user} profile".format(user=self.user)


class CountryCodes(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()