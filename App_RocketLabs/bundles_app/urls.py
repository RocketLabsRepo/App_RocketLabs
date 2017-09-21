# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'bundles_app'

urlpatterns = [
    url(r'^createservice/$', views.create_service_view, name = "create_service"),
    url(r'^services/$', views.services_view, name = "all_services"),
    url(r'^services/([0-9]+)/$', views.detailservice_view, name = "detail_service"),
    url(r'^editservice/([0-9]+)/$', views.editservice_view, name = "edit_service"),
]