from django.contrib.auth.models import User
from django.db import models

# Create your models here.

"""""""""""""""""""""""""""
Request Model

"""""""""""""""""""""""""""
class Request(models.Model):

	requester_name = models.CharField(max_length=30)
	telephone_number = models.DecimalField(max_digits=13, decimal_places=0, blank = True)
	requester_mail = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.CharField(max_length=500)
	sent_date = models.DateTime(auto_now_add = True)
	status = models.CharField(max_length=15)

	def __str__(self):
		return self.requester_mail


"""""""""""""""""""""""""""
Skill Model

"""""""""""""""""""""""""""
class Skill(models.Model):

	name = models.CharField(max_length=50)
	skill_logo = models.ImageField(upload_to="Skill_imgs")
	about = models.CharField(max_length=255)

	def __str__(self):
		return self.name


"""""""""""""""""""""""""""
knows Model

"""""""""""""""""""""""""""
class knows(models.Model):

	exp_level = models.CharField(max_length=30)


"""""""""""""""""""""""""""
Profile Model

"""""""""""""""""""""""""""
class Profile(models.Model):

	company_name = models.CharField(max_length = 70, blank = True)
	title = models.CharField(max_length=30, blank = True)
	linkedln_link = models.CharField(max_length=50, blank = True)
	bio = models.CharField(max_length = 255, blank = True)
	secret_link = models.CharField(max_length = 50)
	photo = models.ImageField(upload_to="profile_imgs", default= "media/default.png")
	is_admin = models.BooleanField(default=False)
	is_team_member= models.BooleanField(default = False)
	failed_logins = models.DecimalField(max_digits=1, decimal_places=0, default=0)
	is_blocked = models.BooleanField(default=False)

	def __str__(self):
		return self.secret_link


"""""""""""""""""""""""""""
Project Model

"""""""""""""""""""""""""""
class Project(models.Model):

	title = models.CharField(max_length=100)
	str_duration = models.CharField(max_length=50, blank = True)
	estimated_duration = models.CharField(max_length=50, blank=True)
	done_percentage = models.DecimalField(max_digits=3, decimal_places=2, blank = True)
	current_stage = models.CharField(max_length=50, blank =True)
	is_complete = models. BooleanField(default = False)
	owner_comment = models.TextField(max_length = 500, blank =True)
	demo_link = models.CharField(max_length = 100, blank = True)
	start_date = models.DateTime(auto_now_add = True)
	finish_date = models.DateTimeField(blank = True)

	def __str__(self):
		return self.title


"""""""""""""""""""""""""""
Screenshot Model

"""""""""""""""""""""""""""
class Screenshot(models.Model):

	name = models.CharField(max_length=50)
	screenshot = models.ImageField(upload_to="Screenshots")
	date_uploaded = models.DateTime(auto_now_add = True)

	def __str__(self):
		return self.name


"""""""""""""""""""""""""""
Bundle Model

"""""""""""""""""""""""""""
class Bundle(models.Model):

	title = models.CharField(max_length = 100)
	about = models.CharField(max_length=255)
	bundle_extra_fee = models.DecimalField(max_digits=4, decimal_places = 2)	#Revisar
	bundle_total_fee = models.DecimalField(max_digits=4, decimal_places= 2)		#Revisar
	is_custom = models.BooleanField()	#Revisar
	is_active = models.BooleanField()	#Revisar

	def __str__(self):
		return self.title


"""""""""""""""""""""""""""
Service Model

"""""""""""""""""""""""""""
class Service(models.Model):

	name = models.CharField(max_length = 50)
	about = models.CharField(max_length = 255)
	visual_aid = models.CharField(upload_to="Service_imgs")
	service_fee = models.CharField(max_digits = 3, decimal_places = 2)
	is_active = models.BooleanField()

	def __str__(self):
		return self.name
