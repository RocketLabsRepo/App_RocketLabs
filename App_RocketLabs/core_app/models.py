from django.contrib.auth.models import User
from django.db import models

# Create your models here.

"""""""""""""""""""""""""""
Request Model

"""""""""""""""""""""""""""
class Request(models.Model):

	project_id = models.ForeignKey(Project, blank = True, default = None)
	client_user = models.ForeignKey(User, blank = True, default = None)
	admin_user = models.ForeignKey(User, blank = True, default = None)

	requester_name = models.CharField(max_length=30)
	telephone_number = models.DecimalField(max_digits=13, decimal_places=0, blank = True)
	requester_mail = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=500)
	sent_date = models.DateTimeField(auto_now_add = True)
	status = models.CharField(max_length=15)

	def __str__(self):
		return self.requester_mail


"""""""""""""""""""""""""""
Skill Model

"""""""""""""""""""""""""""
class Skill(models.Model):

	profiles = models.ManyToManyField(Profile, blank = True, default = None)

	name = models.CharField(max_length=50)
	skill_logo = models.ImageField()
	about = models.TextField(max_length=255)

	def __str__(self):
		return self.name


"""""""""""""""""""""""""""
knows Model

"""""""""""""""""""""""""""
class knows(models.Model):

	user_id = models.ManyToManyField(User) #Revisar
	skill_id = models.ManyToManyField(Skill) #Revisar

	exp_level = models.CharField(max_length=30)


"""""""""""""""""""""""""""
Profile Model

"""""""""""""""""""""""""""
class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)

	company_name = models.CharField(max_length = 70, blank = True)
	title = models.CharField(max_length=30, blank = True)
	linkedln_link = models.CharField(max_length=50, blank = True)
	bio = models.TextField(max_length = 255, blank = True)
	secret_link = models.CharField(max_length = 50, unique=True)
	photo = models.ImageField()
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

	owner_profiles = models.ManyToManyField(Profile)
	bundle = models.ForeignKey(Bundle)

	title = models.CharField(max_length=100)
	description = models.TextField(max_length=255)
	str_duration = models.CharField(max_length=50, blank = True)
	estimated_duration = models.CharField(max_length=50, blank=True)
	done_percentage = models.DecimalField(max_digits=3, decimal_places=2, blank = True)
	current_stage = models.CharField(max_length=50, blank =True)
	is_complete = models. BooleanField(default = False)
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

	project = models.ForeignKey(Project, blank=True, null = True ,default=None)

	name = models.CharField(max_length=50)
	screenshot = models.ImageField()
	date_uploaded = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name


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
