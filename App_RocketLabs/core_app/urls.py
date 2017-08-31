# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [

	url(r'^$', views.home, name='home'),
	url(r'^register/$', views.register_view, name = "Register"),
	url(r'^login/$', views.login_view, name = "Login"),
    url(r'^logout/$', views.logout_view, name='Logout'),
    url(r'^profile/$', views.profile_view, name='Edit_Profile'),
]

# URL para servir las imagenes de forma local durante debug.

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    ]