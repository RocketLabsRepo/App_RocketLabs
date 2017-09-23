# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from bundles_app.models import Bundle, Service



class CreateServiceForm(forms.ModelForm):

	class Meta:
		model = Service	
		
		fields = ['name', 'about', 'is_active']
		
		labels = { 'name':_('Nombre del servicio'),
					'about':_('Descripción'),
					'is_active':_('¿Esta activo?'),}
		
		widgets = {'name': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'about': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'5', 'style':'resize:none'}),
					}

class CreateBundleForm(forms.ModelForm):

	class Meta:
		model = Bundle	
		
		fields = ['title', 'about']
		
		labels = { 'title':_('Titulo del paquete'),
					'about':_('Descripcion'),
				}
		
		widgets = {'title': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'about': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'5', 'style':'resize:none'}),
					}

	def clean_title(self):
		title = self.cleaned_data.get('title')
		if Bundle.objects.filter(title = title).exists():
			raise forms.ValidationError(_("El titulo de este paquete esta en uso, escoja otro."),code="invalid")
		return title

