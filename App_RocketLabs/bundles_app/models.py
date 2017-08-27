# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""""""""""""""""""""""""""
Bundle Model

"""""""""""""""""""""""""""
class Bundle(models.Model):

	title = models.CharField(max_length = 100, unique=True)
	about = models.TextField(max_length=255)
	bundle_extra_fee = models.DecimalField(max_digits=4, decimal_places = 2)
	bundle_total_fee = models.DecimalField(max_digits=4, decimal_places= 2)
	is_custom = models.BooleanField()
	is_active = models.BooleanField(default = True)

	def __str__(self):
		return self.title

"""""""""""""""""""""""""""
Service Model

"""""""""""""""""""""""""""
class Service(models.Model):

	bundle = models.ManyToManyField(Bundle)

	name = models.CharField(max_length = 50)
	about = models.TextField(max_length = 255)
	visual_aid = models.ImageField()
	service_fee = models.DecimalField(max_digits = 3, decimal_places = 2)
	is_active = models.BooleanField(default = True)

	def __str__(self):
		return self.name

