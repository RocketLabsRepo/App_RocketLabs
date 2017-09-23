# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from bundles_app.models import Bundle, Service
import bundles_app.forms as bundle_forms

# Create your views here.


#Vista para crear servicio
@login_required
def service_create_view(request):

	if request.method == 'POST':
		form = bundle_forms.CreateServiceForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, 'Servicio creado con éxito!')
			return redirect('bundles_app:create_service')
		else:
			return render(request, 'bundles_app/create_service.html', {'form': form })

	form = bundle_forms.CreateServiceForm()
	return render(request, 'bundles_app/create_service.html', {'form': form })



def all_services_view(request):
	"""
	Esta view le pasa a la template todos los objetos Service que esten activos.

	"""
	services = Service.objects.filter(is_active=True)
	return render(request, 'bundles_app/all_services.html', {'services': services} )


def service_detail_view (request, service_pk):
	"""
	Esta view le pasa a la template el objeto Service indicado.

	"""
	service_detail = get_object_or_404(Service, pk = service_pk)
	return render(request, 'bundles_app/service_detail.html', {'service_detail': service_detail})

@login_required
def service_edit_view(request, service_pk):
	if request.method == 'POST':	
		service = get_object_or_404(Service, pk = service_pk)
		form = bundle_forms.CreateServiceForm(request.POST, instance = service, prefix='editservice')
		if form.is_valid():
			form.save()
			messages.success(request, 'Se han guardado los cambios en el servicio con exito')
			return HttpResponseRedirect('/services/'+str(service.id))

	else:
		service = get_object_or_404(Service, pk = service_pk)
		form = bundle_forms.CreateServiceForm(instance = service ,prefix='editservice')
		return render(request, 'bundles_app/edit_service.html', {'form':form} )

