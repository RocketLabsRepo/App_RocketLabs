# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# imports de modelos de otras apps.
#from core_app.models import Profile
#from bundles_app.models import Bundle

# Create your models here.


"""""""""""""""""""""""""""
Project Model

"""""""""""""""""""""""""""
class Project(models.Model):

	owner_profiles = models.ManyToManyField('core_app.Profile', db_table ="projects_app_owner_profiles")
	bundle = models.ForeignKey('bundles_app.Bundle', null=True, default=None) # Null y default solo para probar mientras no hay bundles implementados.

	title = models.CharField(max_length=100)
	description = models.TextField(max_length=255)
	str_duration = models.CharField(max_length=50, blank = True)
	estimated_duration = models.CharField(max_length=50, blank=True)
	done_percentage = models.DecimalField(max_digits=3, decimal_places=2, blank = True)
	current_stage = models.CharField(max_length=50, blank =True)
	is_complete = models.BooleanField(default = False)
	owner_comment = models.TextField(max_length = 500, blank =True)
	demo_link = models.CharField(max_length = 100, blank = True)
	last_update_date = models.DateTimeField(auto_now=True)
	start_date = models.DateTimeField(auto_now_add=True)
	finish_date = models.DateTimeField(blank = True)

	def __str__(self):
		return self.title


"""""""""""""""""""""""""""
Screenshot Model

"""""""""""""""""""""""""""
class Screenshot(models.Model):

	project = models.ForeignKey(Project, blank=True, null = True ,default=None, on_delete=models.CASCADE)

	name = models.CharField(max_length=50)
	screenshot = models.ImageField()
	date_uploaded = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name


