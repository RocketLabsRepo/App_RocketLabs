# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

import projects_app.forms as project_forms
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

@login_required
def new_project(request):
	context={}
	go_to_section = False
	if request.method == 'POST':
		proj_form = project_forms.NewProjectForm(request.POST or None)
		if proj_form.is_valid():
			project = proj_form.save()
			user_profile = request.user.profile
			project.owner_profiles.add(user_profile)

			"""
			Here an email is sent to both, the company and the user's email.

			"""
			return redirect('core_app:edit_profile')
		else:
			context['form'] = proj_form
			go_to_section  = 'form'
			context['jump']= go_to_section
			return render(request, 'projects_app/new_project.html',context)
	else:
		proj_form = project_forms.NewProjectForm()
		context['form'] = proj_form
		context['jump']= go_to_section
		return render(request, 'projects_app/new_project.html',context)