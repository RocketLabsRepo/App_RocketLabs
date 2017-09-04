# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render

from projects_app.models import Project
from core_app.models import Skill
# Create your views here.

# Helper function: Yields a generator with objects in l grouped in groups of n.
def grouped(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def home(request):
	context = {}
	# Le pasaremos los ultimos 4 proyectos completados al contexto.
	latests_4 = Project.objects.filter(is_complete = True).order_by('-finish_date')
	latests_4 = latests_4[:4]
	context['latests_projects'] = latests_4

	# Le pasaremos todas las habilidades manejadas por la empresa.
	skills = grouped(Skill.objects.all() , 4)
	context['skill_list'] = skills

	return render(request,'core_app/index.html', context)

