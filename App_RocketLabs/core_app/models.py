# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
#from .views import cod_generator	
import uuid

# imports de modelos de otras apps.
#from bundles_app.models import Bundle
#from projects_app.models import Project


def skill_logo_directory_path(instance, filename):
    # El screenshot será subido a MEDIA_ROOT/project/<id>/<filename>
    return 'skill_logos/{0}/{1}'.format(instance.name, filename)


# Create your models here.


"""""""""""""""""""""""""""
Profile Model

"""""""""""""""""""""""""""
class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)

	company_name = models.CharField(max_length = 70, blank = True)
	title = models.CharField(max_length=100, blank = True)
	linkedln_link = models.CharField(max_length=50, blank = True)
	bio = models.TextField(max_length = 150, blank = True)
	secret_link = models.CharField(max_length = 50, blank = True)
	photo = models.ImageField(blank =True, upload_to = "photo_profile", default = "../media/photo_profile/default-user.png")
	is_admin = models.BooleanField(default=False)
	is_team_member= models.BooleanField(default = False)
	failed_logins = models.SmallIntegerField(default=0)
	is_blocked = models.BooleanField(default=False)

	def __str__(self):

		return "{}'s profile".format(self.user.get_username()).encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Request Model

"""""""""""""""""""""""""""
class Request(models.Model):
	
	requester_name = models.CharField(max_length=30)
	telephone_number = models.CharField(max_length=15)
	requester_mail = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=500)
	sent_date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.subject.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Skill Model

"""""""""""""""""""""""""""
class Skill(models.Model):

	users = models.ManyToManyField(User, through='knows')
	name = models.CharField(max_length=50, unique = True)
	skill_logo = models.ImageField( upload_to = skill_logo_directory_path )
	about = models.TextField(max_length=255, blank=True, default='')

	def __str__(self):
		return self.name.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
knows Model -Es la tabla intermedia de la relacion many2many entre Skill y User

"""""""""""""""""""""""""""
class knows(models.Model):

	EXP = (('Junior Developer', 'Junior Developer'),
				 ('Semi-Senior Developer', 'Semi-Senior Developer'),
				 ('Senior Developer', 'Senior Developer')
		  )

	user = models.ForeignKey(User, limit_choices_to={'profile__is_team_member': True})
	skill = models.ForeignKey(Skill)
	exp_level = models.CharField(max_length=30, choices=EXP, default='Junior Developer')

	class Meta:

		unique_together = (("user", "skill"),)

	def __str__(self):
		return "{} knows {}".format(self.user,self.skill).encode('utf-8', errors='replace')



#esta seccion de codigo nos permite crear un objeto Profile
#por cada objeto User creado en el sistema automaticamente.    
def create_profile(sender, **kwargs):

	def cod_generator(string_length):
		"""Returns a random string of length string_length."""
		random = str(uuid.uuid4()) # Convert UUID format to a Python string.
		random = random.upper() # Make all characters uppercase.
		random = random.replace("-","") # Remove the UUID '-'.
		cod = random[0:string_length] 
		while Profile.objects.filter(secret_link=cod).exists():
			cod = random[0:string_length] 
		return cod # Return the random string.

	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = Profile(user=user)
		user_profile.secret_link = cod_generator(25)
		user_profile.save()
		
post_save.connect(create_profile, sender=User)
