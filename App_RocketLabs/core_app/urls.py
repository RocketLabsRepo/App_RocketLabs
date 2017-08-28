# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'core_app'
urlpatterns = [

	url(r'^$', views.home, name='home'),
    
]