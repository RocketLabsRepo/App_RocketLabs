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
					'about':_('Descripcion'),
					'is_active':_('esta activo?'),}
		
		widgets = {'name': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'about': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'5', 'style':'resize:none'}),
					'is_active':forms.CheckboxInput(attrs={}),
					}


class CreateBundleForm(forms.ModelForm):

	class Meta:
		model = Bundle	
		
		fields = ['title', 'about', 'is_custom','is_active',]
		
		labels = { 'title':_('Titulo del paquete'),
					'about':_('Descripcion'),
					'is_custom':_('Es personalizado'),
					'is_active':_('esta activo?'),}
		
		widgets = {'title': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'about': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'5', 'style':'resize:none'}),
					'is_custom':forms.CheckboxInput(attrs={}),
					'is_active':forms.CheckboxInput(attrs={}),

					}