# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

app_name = 'projects_app'
urlpatterns = [
	url(r'^$', views.all_projects, name='all_projects'),
]