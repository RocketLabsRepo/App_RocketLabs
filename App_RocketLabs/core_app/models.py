# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# imports de modelos de otras apps.
#from bundles_app.models import Bundle
#from projects_app.models import Project


# Create your models here.


"""""""""""""""""""""""""""
Profile Model

"""""""""""""""""""""""""""
class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)

	company_name = models.CharField(max_length = 70, blank = True)
	title = models.CharField(max_length=30, blank = True)
	linkedln_link = models.CharField(max_length=50, blank = True)
	bio = models.TextField(max_length = 255, blank = True)
	secret_link = models.CharField(max_length = 50, unique=True, blank = True)
	photo = models.ImageField(blank =True)
	is_admin = models.BooleanField(default=False)
	is_team_member= models.BooleanField(default = False)
	failed_logins = models.DecimalField(max_digits=1, decimal_places=0, default=0)
	is_blocked = models.BooleanField(default=False)

	def __str__(self):
		return "{}'s profile".format(self.user.get_username())


"""""""""""""""""""""""""""
Request Model

"""""""""""""""""""""""""""
class Request(models.Model):

	#project_id = models.ForeignKey(Project, blank = True, default = None)
	client_user = models.ForeignKey(User, blank = True, default = None)
	

	requester_name = models.CharField(max_length=30)
	telephone_number = models.DecimalField(max_digits=13, decimal_places=0, blank = True)
	requester_mail = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=500)
	sent_date = models.DateTimeField(auto_now_add = True)
	

	def __str__(self):
		return self.requester_mail


"""""""""""""""""""""""""""
Skill Model

"""""""""""""""""""""""""""
class Skill(models.Model):

	users = models.ManyToManyField(User, through='knows')

	name = models.CharField(max_length=50)
	skill_logo = models.ImageField()
	about = models.TextField(max_length=255)

	def __str__(self):
		return self.name


"""""""""""""""""""""""""""
knows Model -Es la tabla intermedia de la relacion many2many entre Skill y User

"""""""""""""""""""""""""""
class knows(models.Model):

	user = models.ForeignKey(User)
	skill = models.ForeignKey(Skill)

	exp_level = models.CharField(max_length=30)

#esta seccion de codigo nos permite crear un objeto Profile
#por cada objeto User creado en el sistema automaticamente.
def create_profile(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = Profile(user=user)
		user_profile.save()
		
post_save.connect(create_profile, sender=User)
