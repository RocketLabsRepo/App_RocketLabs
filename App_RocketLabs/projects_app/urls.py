# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^projects/$', views.all_projects, name='all_projects'),
]