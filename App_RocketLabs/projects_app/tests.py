# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core_app.models import Profile
from projects_app.models import Project, Screenshot

# Create your tests here.

"""""""""""""""""""""""""""
Global helper functions

"""""""""""""""""""""""""""

def create_project(user,  ptitle):
	user_profile = user.profile
	project = Project.objects.create(title=ptitle)
	project.owner_profiles.add(user_profile)
	return project


"""""""""""""""""""""""""""
Views Tests

"""""""""""""""""""""""""""

class AllProjectsPageTest(TestCase):

	def test_all_projects_page_returns_correct_html(self):
		response = self.client.get('/projects/') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/projects.html')

	def test_displays_all_completed_projects(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

		create_project(user,'Project One')
		create_project(user,'Project Two')

		response = self.client.get('/projects/')

		self.assertIn('Project One' , response.content.decode('utf-8') , "'{0}' did not appear in Page content".format('Project One'))
		self.assertIn('Project Two' , response.content.decode('utf-8') ,"'{0}' did not appear in Page content".format('Project Two'))		

	def test_message_shows_with_no_project_to_display(self):

		response = self.client.get('/projects/')

		self.assertEqual(Project.objects.count() , 0)
		self.assertIn("Lo sentimos, actualmente no tenemos proyectos disponibles." , response.content.decode('utf-8') , "No hay mensaje sin proyectos.")

class DetailsProjectsPageTest(TestCase):

	def test_project_details_page_returns_correct_html(self):
		response = self.client.get('/projects/id') #implicit test_project_details_url_resolves_to_project_details_view
		self.assertTemplateUsed(response, 'projects_app/project_details.html')


"""""""""""""""""""""""""""
Models Tests

"""""""""""""""""""""""""""

class ProjectModelTest(TestCase):

	def test_can_create_and_retrieve_projects(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user_profile = user.profile

		project1 = Project.objects.create(title="This is a Project")
		project1.owner_profiles.add(user_profile)

		project2 = Project.objects.create(title="This is another Project")
		project2.owner_profiles.add(user_profile)

		saved_projects = Project.objects.all()
		owner_projects = user_profile.project_set.all()
		self.assertEqual(saved_projects.count(), 2)
		self.assertEqual(owner_projects.count(), 2)

		first_saved_project = saved_projects[0]
		second_saved_project = saved_projects[1]
		self.assertEqual(first_saved_project.title, 'This is a Project')
		self.assertEqual(second_saved_project.title, 'This is another Project')

	
class ScreenshotModelTest(TestCase):

	# Ligero problema, este test crea archivos en la carpeta media y no los elimina, podria 
	# sobre escribir archivos ya presentes.
	def test_project_can_have_and_retrieve_screenshot_attached(self):

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		project = create_project(user ,'This is a Project')
		screenshot = Screenshot()
		screenshot.name = "A test Screenshot"
		screenshot.project = project

		image = open('core_app/static/core_app/img/foro_estudiantil.png')
		screenshot.img = SimpleUploadedFile(image.name, image.read())
		screenshot.save()

		self.assertEqual(Screenshot.objects.count(), 1)

		saved_screenshot = Screenshot.objects.first()
		self.assertEqual(saved_screenshot.name , "A test Screenshot")

		project_with_screen_saved = Project.objects.get(screenshot__pk=screenshot.id)
		self.assertEqual(project , project_with_screen_saved)
	########
		first_screenshot_of_project = project_with_screen_saved.screenshot_set.first()
		self.assertEqual("A test Screenshot" , first_screenshot_of_project.name)
