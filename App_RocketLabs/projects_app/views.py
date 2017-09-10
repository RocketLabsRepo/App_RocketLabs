# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from projects_app.models import Project
# Helper function: Yields a generator with objects in l grouped in groups of n.
def grouped(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Create your views here.

def all_projects(request):
	context = {'project_list': grouped(Project.objects.filter(is_complete = True).order_by('finish_date'), 4) }
	return render(request,'projects_app/completed_projects.html', context)

def completed_project_details(request, project_pk):
	proj = get_object_or_404(Project , pk=project_pk)
	latests_4 = Project.objects.filter(is_complete = True).exclude(pk=project_pk).order_by('-finish_date')
	latests_4 = latests_4[:4]

	if proj.is_complete:
		context = {'project': proj,'latests':latests_4}
	else:
		context = {'project': None, 'latests':latests_4}
	return render(request,'projects_app/completed_project_details.html',context)
