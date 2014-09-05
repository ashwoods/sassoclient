from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

from django.contrib.auth.backends import ModelBackend
from django.conf import settings


class SSOUserBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True
    try:
        secret_key = settings.SASSO_SECRET_KEY
    except AttributeError:
        raise ImproperlyConfigured("In order to authenticate SASSO remote users you need to set SASSO_SECRET_KEY in settings")

    def authenticate(self, sso_id, sso_email, sso_token):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not sso_id:
            return
        user = None

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.

        # TODO: if a user doesn't exist, create one with a random username (empty email)
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD:
            })
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass
        return user

    def configure_user(self, user): # TODO: add email to user object from header
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        return user
