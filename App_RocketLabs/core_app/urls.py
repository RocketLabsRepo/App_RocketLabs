# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include

app_name = 'core_app'
urlpatterns = [

	url(r'^$', views.home, name='home'),
	url(r'^register/$', views.register_view, name = "register"),
	url(r'^login/$', views.login_view, name = "login"),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile_view, name='edit_profile'),
    url(r'^team/$', views.allteammember_view, name='all_team_members'),
    url(r'^team/([0-9]+)/$', views.detailsteammember_view, name='details_team_member'),
    url(r'^changepassword/$', views.changepassword_view, name = "changepass"),
]

# URL para servir las imagenes de forma local durante debug.

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    ]