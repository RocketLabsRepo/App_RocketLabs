# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib import admin
from core_app.models import Profile, Request, Skill, knows
# Register your models here.

admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(Skill)
admin.site.register(knows)

