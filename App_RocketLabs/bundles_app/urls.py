# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createservice/$', views.create_service_view, name = "create_service"),
    url(r'^services/$', views.services_view, name = "all_services"),
]