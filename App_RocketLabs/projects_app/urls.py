# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'projects_app'
urlpatterns = [
	url(r'^$', views.all_projects, name='all_completed_projects'),
	url(r'^(?P<project_pk>\d+)$', views.completed_project_details, name='completed_project_details'),
	url(r'^new$', views.new_project, name='new_project'),
]
"""
urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    ]
"""

