# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios

from projects_app.models import Project


# Formulario para emitir un nuevo proyecto
class NewProjectForm(forms.ModelForm):

	class Meta:
		model = Project

		fields = ['title', 'description', 'bundle']

		labels = {  'title':_('Crea un título para tu proyecto'),
					'description':_('Ofrece una breve descripción del proyecto'),
					'bundle':_('Selecciona un paquete de trabajo'),
				}

		widgets = {	'title': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'description': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'3', 'style':'resize:none' }),
					'bundle': forms.Select(attrs={'class':'w3-input w3-border input-font'}),
				}

	terms_confirm = forms.BooleanField(required=True, label="Acepto los Términos y Condiciones de Uso.")

	def clean_title(self):
		data = self.cleaned_data["title"]
		if Project.objects.filter(title=data).exists():
			raise forms.ValidationError(_("Este título ya esta en uso, por favor escoge otro."),code="invalid")
		return data