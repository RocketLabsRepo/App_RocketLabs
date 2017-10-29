# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios
from django.forms.models import inlineformset_factory

from core_app.models import Profile, Request


# Formulario para registrar un usuario
class RegisterUserForm(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Nombre de Usuario"
		self.fields['password1'].label = "Contraseña"
		self.fields['password2'].label = "Confirmar contraseña"
		self.fields['username'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['last_name'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['first_name'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['email'].widget = forms.EmailInput(attrs={'class':'w3-input w3-border input-font', 'placeholder':'ejemplo@email.com'})
	
	first_name = forms.CharField(label="Nombre",max_length=30) #, help_text="Opcional", required = False
	last_name = forms.CharField(label="Apellido",max_length=30) #, help_text="Opcional", required = False
	email = forms.EmailField(label="Correo Electrónico", max_length=254, required=True)

	class Meta:
		model = User
		fields = ('first_name','last_name','email','username','password1','password2',)

	#Verifica que el nombre de usuario sea único
	def clean_username(self):
		username = self.cleaned_data["username"]

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError( _("Este nombre de usuario ya esta en uso, escoja otro."),code='duplicate_username')
		
		return username 

	#Verifica que el email es único
	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError(_("Dirección de correo ya esta en uso, escoja otra."),code="invalid")
		return data

	#Verifica que las contraseñas coincidan
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError(_("¡Debes repetir tu contraseña!"))
		if password1 != password2:
			raise forms.ValidationError(_("Las contraseñas nos son iguales."))
		return password2


# Formulario para iniciar sesión.
my_default_errors = {
    'required': 'Por favor rellene este campo.',
    'invalid': 'Por favor ingrese un valor válido.'
}

class LoginForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['usernameLogin'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['passwordLogin'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		

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
				raise forms.ValidationError(_("Usuario o contraseña inválida. Por favor intente de nuevo."), code='invalido')
			else:
				profile.failed_logins = 0
				profile.save()
			return self.cleaned_data
		else:
			raise forms.ValidationError(_("Usuario o contraseña inválida. Por favor intente de nuevo."), code='invalido')


	def login(self, request):
		username = self.cleaned_data.get('usernameLogin')
		password = self.cleaned_data.get('passwordLogin')
		user = authenticate(username=username, password=password)
		return user

#Formulario para desplegar Perfil de usuario Promedio
class EditClientProfileForm(forms.ModelForm):

	class Meta:
		model = Profile	
		
		fields = ['company_name']
		labels = { 'company_name': _('Nombre de mi empresa'),}
		widgets = {'company_name': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),}

class EditTeamMemberForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		
		fields = ['linkedln_link', 'photo', 'bio']
		labels = { 	'linkedln_link': _('Perfil Linkedin'),
					'photo': _('Foto'),
					'bio': _('Acerca de mi'),
				}
		widgets = {	'linkedln_link': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'photo': forms.FileInput(attrs={'class':'w3-input w3-border input-font' }),
					'bio': forms.Textarea(attrs={'class':'w3-input w3-border input-font', 'rows':'5', 'style':'resize:none' }),
				}



class EditUserForm(forms.ModelForm):

	class Meta:
		model = User

		fields = ['first_name', 'last_name']

		labels = {'first_name':_('Nombre'),
					'last_name':_('Apellido'),
				}

		widgets = {'first_name': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
					'last_name': forms.TextInput(attrs={'class':'w3-input w3-border input-font' }),
				}

#Formulario para cambiar la contraseña.
class ChangePassForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super(ChangePassForm, self).__init__(*args, **kwargs)
		self.fields['old_password'].label = "Contraseña actual"
		self.fields['new_password1'].label = "Nueva contraseña"
		self.fields['new_password2'].label = "Confirmar contraseña"

		self.fields['old_password'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})

	#Este codigo no lanza el mensaje
	def clean_old_password(self):
		password = self.cleaned_data['old_password']
		if not self.user.check_password(password):
			print ("La Contraseña es invalida: Old Password")
			raise forms.ValidationError(_("La contraseña es incorrecta."),code='invalid_password')
		return password

	#Este codigo no lanza el mensaje.
	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 != password2:
			raise forms.ValidationError(_("Las nuevas contraseñas no coinciden."), code = "new_password")
		return password2

# Formulario para definir la contraseña de una cuenta por primera vez.
class DefinePassForm(AdminPasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super(DefinePassForm, self).__init__(*args, **kwargs)
		
		self.fields['password1'].label = "Contraseña"
		self.fields['password2'].label = "Confirmar contraseña"
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'w3-input w3-border input-font'})

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError(_("Las nuevas contraseñas no coinciden."), code = "new_password")
		return password2


class ContactForm(forms.ModelForm):

	class Meta:
		model = Request

		fields = ['requester_name', 'requester_mail', 'telephone_number', 'subject', 'message']

		labels = {	'requester_name':_('Nombre de contacto'),
					'requester_mail':_('Correo Electrónico'),
					'telephone_number':_('Teléfono'),
					'subject':_('Asunto'),
					'message':_('Mensaje'),
				}
		
		widgets = {	'requester_name': forms.TextInput(attrs={'class':'w3-input input-font' }),
					'requester_mail': forms.EmailInput(attrs={'class':'w3-input input-font' }),
					'telephone_number': forms.TextInput(attrs={'class':'w3-input input-font','pattern':'\d{7,15}','placeholder':'Solo números.' }),
					'subject': forms.TextInput(attrs={'class':'w3-input input-font' }),
					'message': forms.Textarea(attrs={'class':'w3-input input-font', 'rows':'5', 'placeholder':'Máximo 500 caracteres.' }),
				}


#Formulario para recuperar contraseña
class RecoverPassForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(RecoverPassForm, self).__init__(*args, **kwargs)
		self.fields['user'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		self.fields['secret_link'].widget = forms.TextInput(attrs={'class':'w3-input w3-border input-font'})
		

	user = forms.CharField(label="Nombre de usuario", max_length=64, required=True, error_messages=my_default_errors)
	secret_link = forms.CharField(label="Código único", max_length = 25, required=True, error_messages=my_default_errors)




#Formulario para enviar codigounico
class RecoverSecretLinkForm(forms.ModelForm):

	class Meta:
		model = User

		fields = ['email']

		labels = { 'email':_('Correo Electrónico'),}

		widgets = {	'email': forms.EmailInput(attrs={'class':'w3-input w3-border input-font' }),}

# Formulario para cambiar el email
class ChangeEmailForm(forms.ModelForm):

	class Meta:
		model = User

		fields = ['email']

		labels = { 'email':_('Correo Electrónico'),}

		widgets = {	'email': forms.EmailInput(attrs={'class':'w3-input w3-border input-font' }),}

	email_confirm = forms.EmailField(label="Repetir correo",widget=forms.EmailInput(attrs={'class':'w3-input w3-border input-font'}))

	def clean_email(self):
		email = self.cleaned_data['email']
		# Si el email ya esta en uso, levantamos un error.
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(_("Dirección de correo ya esta en uso, escoja otra."),code="invalid")
		return email

	def clean_email_confirm(self):
		email1 = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email_confirm')
		if email1 != email2:
			raise forms.ValidationError(_("Los correos electrónicos no coinciden."), code = "no_match")
		return email2