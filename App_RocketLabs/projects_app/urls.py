# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'projects_app'
urlpatterns = [
	url(r'^$', views.all_projects, name='all_completed_projects'),
	url(r'^id$', views.project_details, name='project_details')
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    ]