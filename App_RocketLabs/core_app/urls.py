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
    
]