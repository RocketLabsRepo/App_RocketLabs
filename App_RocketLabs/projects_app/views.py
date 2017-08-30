# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from projects_app.models import Project
# Helper function: Yields a generator with objects in l grouped in groups of n.
def grouped(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Create your views here.

def all_projects(request):
	context = {'project_list': grouped(Project.objects.filter(is_complete = True).order_by('id'), 4) }
	return render(request,'projects_app/projects.html', context)

def project_details(request):
	return render(request,'projects_app/project_details.html')
