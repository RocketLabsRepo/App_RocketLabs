# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib import admin
from core_app.models import Profile
# Register your models here.

admin.site.register(Profile)