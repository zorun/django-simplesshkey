# Copyright (c) 2017, Baptiste Jonglez
# Copyright (c) 2014-2016, Clemson University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Clemson University nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from django.db import models
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from simplesshkey.util import PublicKeyParseError, pubkey_parse


class AbstractUserKey(models.Model):
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, db_index=True,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    key = models.TextField(max_length=2000)
    fingerprint = models.CharField(max_length=128, blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.user) + u': ' + self.name

    def clean_fields(self, exclude=None):
        if not exclude or 'key' not in exclude:
            self.key = self.key.strip()
            if not self.key:
                raise ValidationError({'key': ["This field is required."]})

    def clean(self):
        self.key = self.key.strip()
        if not self.key:
            return
        try:
            pubkey = pubkey_parse(self.key)
        except PublicKeyParseError as e:
            raise ValidationError(str(e))
        self.key = pubkey.format_openssh()
        self.fingerprint = pubkey.fingerprint()
        if not self.name:
            if pubkey.comment:
                self.name = pubkey.comment

    def export(self, format='RFC4716'):
        pubkey = pubkey_parse(self.key)
        f = format.upper()
        if f == 'RFC4716':
            return pubkey.format_rfc4716()
        if f == 'PEM':
            return pubkey.format_pem()
        raise ValueError("Invalid format")


class UserKey(AbstractUserKey):
    pass
