# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.core import validators
from django.db import models
from django.utils.http import urlquote

from model_utils.models import TimeStampedModel

from autoslug import AutoSlugField
from djorm_hstore.models import HStoreManager
from djorm_hstore.fields import DictionaryField

from .conf import settings
from autoslug.utils import translit_long
from uuidfield import UUIDField
from model_utils.fields import AutoLastModifiedField

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    sso_id = UUIDField(unique=True, null=True)

    class Meta:
        db_table = 'auth_user'




#
# @python_2_unicode_compatible
# class AbstractSSOUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.
#
#     Username, password and email are required. Other fields are optional.
#     """
#     username = models.CharField(_('username'), max_length=30, unique=True,
#         help_text=_('Required. 30 characters or fewer. Letters, numbers and '
#                     '@/./+/-/_ characters'),
#         validators=[
#             validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
#         ])
#
#     email = models.EmailField(_('email address'), max_length=255, unique=False,
#                               db_index=True, blank=True)
#
#     sso_id = UUIDField(unique=True, blank=True, null=True)
#     is_staff = models.BooleanField(_('staff status'), default=False,
#         help_text=_('Designates whether the user can log into this admin '
#                     'site.'))
#     is_active = models.BooleanField(_('active'), default=True,
#         help_text=_('Designates whether this user should be treated as '
#                     'active. Unselect this instead of deleting accounts.'))
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#     modified = AutoLastModifiedField(_('modified'))
#
#     #objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#     #REQUIRED_FIELDS = ['sso_id']
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#         abstract = True
#
#     def get_absolute_url(self):
#         return "/users/%s/" % urlquote(self.sso_id)
#
#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in between.
#         """
#         return self.username
#
#     def get_short_name(self):
#         "Returns the short name for the user."
#         return self.username
#
#     def email_user(self, subject, message, from_email=None):
#         """
#         Sends an email to this User.
#         """
#         pass
#         #send_mail(subject, message, from_email, [self.email])
#
#     def get_profile(self):
#         """
#         Returns site-specific profile for this user. Raises
#         SiteProfileNotAvailable if this site does not allow profiles.
#         """
#         pass
#         #return self._profile_cache
#
#     def __str__(self):
#         return self.sso_id
#
#
# class User(AbstractSSOUser):
#
#     class Meta(AbstractSSOUser.Meta):
#         swappable = 'AUTH_USER_MODEL'
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#
#         db_table = 'auth_user'
