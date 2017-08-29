# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from core_app.models import Profile
from projects_app.models import Project, Screenshot
# Create your tests here.

"""""""""""""""""""""""""""
Page Tests

"""""""""""""""""""""""""""

class AllProjectsPageTest(TestCase):

	def test_all_projects_page_returns_correct_html(self):
		response = self.client.get('/projects/') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/projects.html')

class DetailsProjectsPageTest(TestCase):

	def test_project_details_page_returns_correct_html(self):
		response = self.client.get('/projects/id') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/project_details.html')


"""""""""""""""""""""""""""
Models Tests

"""""""""""""""""""""""""""

class ProjectModelTest(TestCase):

	def test_can_create_and_retrieve_project(self):
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

	def test_can_create_and_retrieve_screenshot(self):
		pass




"""""""""""""""""""""""""""
View Tests

"""""""""""""""""""""""""""