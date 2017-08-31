# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render

from projects_app.models import Project
# Create your views here.

def home(request):
	# Le pasaremos los ultimos 4 proyectos completados al contexto.
	latests_4 = Project.objects.filter(is_complete = True).order_by('-finish_date')
	latests_4 = latests_4[:4]
	context = {'latests_projects':latests_4}

	return render(request,'core_app/index.html', context)