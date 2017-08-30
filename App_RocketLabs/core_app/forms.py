#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios
from django.forms.models import inlineformset_factory
from .models import Profile
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


# Formulario para iniciar sesión.
my_default_errors = {
    'required': 'Por favor rellene este campo.',
    'invalid': 'Por favor ingrese un valor válido.'
}

class LoginForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['usernameLogin'].widget = forms.TextInput(attrs={'class':'form-control'})
		self.fields['passwordLogin'].widget = forms.PasswordInput(attrs={'class':'form-control'})
		

	usernameLogin = forms.CharField(label="Usuario", max_length=64, required=True, error_messages=my_default_errors)
	passwordLogin = forms.CharField(label="Contraseña", required=True, error_messages=my_default_errors) 
	
	#Este metodo es llamado para validar el formulario y nos permite verificar si el usuario existe o no.
	def clean(self):
		username = self.cleaned_data.get('usernameLogin')
		password = self.cleaned_data.get('passwordLogin')
		user = authenticate(username=username, password=password)
		
		if User.objects.filter(username = username).exists():
			sanctioned = User.objects.get(username = username)
			profile = Profile.objects.get(user = sanctioned.id)
			if sanctioned and profile.is_blocked:
				raise forms.ValidationError(_("El usuario ingresado esta bloqueado!"), code='bloqueado')

			if not user:
				if sanctioned and not profile.is_blocked: #Si esta el usuario registrado pero no bloqueado
					profile.failed_logins +=  1

					if profile.failed_logins > 4:
						profile.is_blocked = True
						profile.failed_logins = 0
						
					profile.save()
					print (profile.is_blocked)
				raise forms.ValidationError(_("Informacion invalida. Por favor intente de nuevo."), code='invalido')
			else:
				profile.failed_logins = 0
				profile.save()
			return self.cleaned_data
		else:
			raise forms.ValidationError(_("Informacion invalida. Por favor intente de nuevo."), code='invalido')


	def login(self, request):
		username = self.cleaned_data.get('usernameLogin')
		password = self.cleaned_data.get('passwordLogin')
		user = authenticate(username=username, password=password)
		return user

#Formulario para desplegar Perfil de usuario Promedio
class EditClientProfileForm(forms.ModelForm):

	class Meta:
		model = Profile	
		
		fields = ['company_name', 'secret_link']
		
		labels = { 'company_name': _('Nombre de la empresa'),
					'secret_link': _('Código unico'),				   
				}
		widgets = {'company_name': forms.TextInput(attrs={'class':'form-control' }),
					'secret_link': forms.TextInput(attrs={'class':'form-control', 'readonly' : True }),}

		"""
		widgets = {'company_name': forms.TextInput(attrs={'placeholder': company_name,'class':'form-control' }),
					'secret_link': forms.TextInput(attrs={'placeholder': secret_link,'class':'form-control', 'readonly' : True }),
				}
		"""

class EditUserForm(forms.ModelForm):

	class Meta:
		model = User

		fields = ['first_name', 'last_name', 'email']

		labels = {'first_name':_('Nombre'),
					'last_name':_('Apellido'),
					'email':_('Correo Electronico'),
				}
		
		widgets = {'first_name': forms.TextInput(attrs={'class':'form-control' }),
					'last_name': forms.TextInput(attrs={'class':'form-control' }),
					'email_name': forms.TextInput(attrs={'class':'form-control' }),
				}


		"""
		widgets = {'first_name': forms.TextInput(attrs={'placeholder': first_name,'class':'form-control' }),
					'last_name': forms.TextInput(attrs={'placeholder': last_name,'class':'form-control' }),
					'email_name': forms.TextInput(attrs={'placeholder': email,'class':'form-control' }),
					}
		"""