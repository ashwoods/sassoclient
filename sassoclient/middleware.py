# -*- coding: utf-8 -*-
from urlparse import urlsplit
import base64, hashlib, hmac, redis, json
from django.http import QueryDict, HttpResponse
from django.conf import settings


from django.contrib import auth
from django.contrib.auth import load_backend
from .backends import SSOUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import constant_time_compare
from django.utils.functional import SimpleLazyObject


from django.core.exceptions import ImproperlyConfigured
import warnings

SSO_KEY = "this is a very secret !"


class SSOSessionMiddleware(object):

    sso_id = "SSO_UUID"
    sso_email = "SSO_EMAIL"
    sso_token = "SSO_TOKEN"


    def process_request(self, request, *args, **kwargs):
        """
        Checks that the signature is valid. The signature has to be set in a
        request header called SSO_SIGNATURE.
        """
        # try:
        #     token = request.META['HTTP_SSO_SIGNATURE']
        #     signed, unsigned = token.split(':', 1)
        # except KeyError:
        #     return HttpResponse('You should not be here!')
        # # Sign with the SSO_KEY
        # s = base64.b64encode(hmac.new(SSO_KEY, unsigned, hashlib.sha1).digest())
        #
        # if signed != s:
        #     return HttpResponse('Tampering attempt detected!') # TODO: raise 401
        # pass


    # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            sso_id = request.META[self.sso_id]
            sso_email = request.META[self.sso_email]
            sso_token = request.META[self.sso_token]

        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(sso_id, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(sso_id=sso_id, sso_email=sso_email, sso_token=sso_token)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, SSOUserBackend):
                auth.logout(request)
