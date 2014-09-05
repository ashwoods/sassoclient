from django.conf.urls import *
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from officium import views as officium_views

urlpatterns = patterns('',
    # Signup, signin and signout
    url(r'^signup/$',
       officium_views.signup,
       name='officium_signup'),
    url(r'^signin/$',
       officium_views.signin,
       name='officium_signin'),
    url(r'^signout/$',
       officium_views.signout,
       name='officium_signout'),


    # Edit profile
    url(r'^(?P<username>[\.\w-]+)/edit/$',
       officium_views.profile_edit,
       name='officium_profile_edit'),

    # View profiles
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
       officium_views.profile_detail,
       name='officium_profile_detail'),
)
