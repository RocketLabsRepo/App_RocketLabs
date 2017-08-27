#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios

# Formulario para registrar un usuario
class RegisterUserForm(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Nombre de Usuario"
		self.fields['password1'].label = "Contraseña"
		self.fields['password2'].label = "Confirmar contraseña"
		self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
		self.fields['last_name'].widget = forms.TextInput(attrs={'class':'form-control'})
		self.fields['first_name'].widget = forms.TextInput(attrs={'class':'form-control'})
		self.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ejemplo@email.com'})
	
	first_name = forms.CharField(label="Nombre",max_length=30, help_text="Opcional", required = False)
	last_name = forms.CharField(label="Apellido",max_length=30, help_text="Opcional", required = False)
	email = forms.EmailField(label="Correo Electrónico", max_length=254, required=True)

	class Meta:
		model = User
		fields = ('first_name','last_name','email','username','password1','password2',)

#Verifica que el nombre de usuario sea único
	def clean_username(self):
		username = self.cleaned_data["username"]

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError( _("Este nombre de usuario ya esta en uso, escoga otro."),code='duplicate_username')
		
		return username 

#Verifica que el email es único
	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError(_("Dirección de correo ya esta en uso, escoga otra."),code="invalid")
		return data

#Verifica que las contraseñas coincidan
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("¡Debes repetir tu contraseña!")
		if password1 != password2:
			raise forms.ValidationError("¡Las contraseñas nos son iguales!")
		return password2