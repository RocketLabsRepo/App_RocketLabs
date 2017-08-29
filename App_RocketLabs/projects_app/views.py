# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def all_projects(request):
	return render(request,'projects_app/projects.html')

def project_details(request):
	return render(request,'projects_app/project_details.html')
