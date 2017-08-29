# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

"""""""""""""""""""""""""""
Page Tests

"""""""""""""""""""""""""""

class AllProjectsPage(TestCase):

	def test_all_projects_page_returns_correct_html(self):
		response = self.client.get('/projects/') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/projects.html')

class DetailsProjectsPage(TestCase):

	def test_project_details_page_returns_correct_html(self):
		response = self.client.get('/projects/id') #implicit test_all_projects_url_resolves_to_all_projects_view
		self.assertTemplateUsed(response, 'projects_app/project_details.html')


"""""""""""""""""""""""""""
Models Tests

"""""""""""""""""""""""""""


"""""""""""""""""""""""""""
View Tests

"""""""""""""""""""""""""""