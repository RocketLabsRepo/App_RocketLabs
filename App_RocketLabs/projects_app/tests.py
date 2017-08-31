# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
import tempfile

from core_app.models import Profile
from projects_app.models import Project, Screenshot


# Create your tests here.

"""""""""""""""""""""""""""
Global helper functions

"""""""""""""""""""""""""""

SCREENSHOT_PATH = 'core_app/static/core_app/img/foro_estudiantil.png'

def create_project(user,  ptitle):
	user_profile = user.profile
	project = Project.objects.create(title=ptitle)
	project.owner_profiles.add(user_profile)
	return project

def complete_project(project):
	project.is_complete = True
	project.finish_date = datetime.now()
	project.save()
	return project

def create_screenshot(project , name):
	image = open(SCREENSHOT_PATH)
	screenshot = Screenshot()
	screenshot.name = name
	screenshot.project = project
	screenshot.img = SimpleUploadedFile(image.name, image.read())
	screenshot.save()
	return screenshot


"""""""""""""""""""""""""""
Views Tests

"""""""""""""""""""""""""""

class AllProjectsPageTest(TestCase):

	def test_all_projects_page_returns_correct_html(self):
		response = self.client.get('/projects/') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/projects.html')

	def test_displays_all_completed_projects(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		project1 = create_project(user,'Project One')
		project2 = create_project(user,'Project Two')
		project3 = create_project(user,'Project Three')

		complete_project(project1)
		complete_project(project2)
		response = self.client.get('/projects/')

		self.assertTrue(project1.is_complete)
		self.assertTrue(project2.is_complete)
		self.assertIn('Project One' , response.content.decode('utf-8') , "'{0}' did not appear in Page content".format('Project One'))
		self.assertIn('Project Two' , response.content.decode('utf-8') ,"'{0}' did not appear in Page content".format('Project Two'))		
		self.assertNotIn('Project Three', response.content.decode('utf-8'), "Project 3 appears even tho' it's not complete.")

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
		project1 = create_project(user,"This is a Project")
		project2 = create_project(user,"This is another Project")

		saved_projects = Project.objects.all()
		owner_projects = user_profile.project_set.all()
		self.assertEqual(saved_projects.count(), 2)
		self.assertEqual(owner_projects.count(), 2)

		first_saved_project = saved_projects[0]
		second_saved_project = saved_projects[1]
		self.assertEqual(first_saved_project.title, 'This is a Project')
		self.assertEqual(second_saved_project.title, 'This is another Project')

	@override_settings(MEDIA_ROOT=tempfile.gettempdir())
	def test_can_return_preview_screenshot(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		project = create_project(user ,'This is a Project')

		screenshot = create_screenshot(project , "A test Screenshot")
		screenshot.is_preview = True
		screenshot.save()

		saved_preview = project.get_preview_screenshot()

		self.assertEqual(saved_preview.name , "A test Screenshot")
		self.assertTrue(saved_preview.is_preview)


	
class ScreenshotModelTest(TestCase):

	@override_settings(MEDIA_ROOT=tempfile.gettempdir())
	def test_project_can_have_and_retrieve_screenshot_attached(self):

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		project = create_project(user ,'This is a Project')
		screenshot = create_screenshot(project , "A test Screenshot")

		self.assertEqual(Screenshot.objects.count(), 1)

		saved_screenshot = Screenshot.objects.first()
		self.assertEqual(saved_screenshot.name , "A test Screenshot")

		project_with_screen_saved = Project.objects.get(screenshot__pk=screenshot.id)
		self.assertEqual(project , project_with_screen_saved)

	@override_settings(MEDIA_ROOT=tempfile.gettempdir())
	def test_mark_as_only_preview_method(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		project = create_project(user ,'This is a Project')
		screenshot1 = create_screenshot(project , "A test Screenshot")
		screenshot2 = create_screenshot(project , "A second test Screenshot")

		screenshot1.mark_as_only_preview()
		screenshot2.mark_as_only_preview()
		project_screens = project.screenshot_set.filter(is_preview=True)

		self.assertEqual(project_screens.count() , 1)
		self.assertEqual(project_screens[0].name , "A second test Screenshot")
