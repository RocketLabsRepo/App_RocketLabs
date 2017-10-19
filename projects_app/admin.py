# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from projects_app.models import Screenshot, Project
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('start_date',)

admin.site.register(Screenshot)
admin.site.register(Project, ProjectAdmin)