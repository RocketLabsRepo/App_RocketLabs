# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginForm, EditUserForm, EditClientProfileForm, EditTeamMemberForm
from .models import Profile
import uuid


# ########################################################Funciones adicionales########################################################################
def cod_generator(string_length=25):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    cod = random[0:string_length] 
    while Profile.objects.filter(secret_link=cod).exists():
    	cod = random[0:string_length] 
    return cod # Return the random string.
##########################################################################################################################################################


# Create your views here.

def home(request):
	return render(request,'core_app/index.html')


# View para desplegar el formulario de registro de usuarios y atender las peticiones de registro
def register_view(request):
	if request.method == 'POST':
		ruf = RegisterUserForm(request.POST)
		if ruf.is_valid():
			user = ruf.save()
			#Generación del código único
			unique_code = cod_generator(25)
			user_profile = user.profile
			user_profile.secret_link = unique_code
			user_profile.save()

			# Ahora una vez creado el usuario y su perfil procederemos a enviarle un mensaje
			# al email indicado con sus credenciales.
			
			"""
			context = {'username':ruf.cleaned_data['username'] ,'password':ruf.cleaned_data['password1']}
			
			msg_plain = render_to_string('registration/user_register_email.txt', context)
			msg_html = render_to_string('registration/user_register_email.html', context)
			
			send_mail(
					'Bienvenido a RocketLabs!', 	#titulo
					msg_plain,							#mensaje txt
					'RockectLabs@gmail.com',		#email de envio
					[user.email],						#destinatario
					html_message=msg_html,				#mensaje en html
					)
			"""
			
			return HttpResponseRedirect('/login')
		else:
			return render(request,'core_app/register.html', {'registeruserform':ruf, }) #'loginf': loginf (Futuro segundo parametro)
	else:
		ruf = RegisterUserForm()
			#Si un usuario con sesión iniciada llega a esta página, se le cerrará la sesión.
		if request.user.is_authenticated:
			logout(request)

		return render(request, 'core_app/register.html', {'registeruserform':ruf,}) #'loginf': loginf (Futuro segundo parametro)


# View para autenticar usuarios e iniciar sesión
def login_view(request):
	
	form = LoginForm(request.POST or None)

	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return redirect('/')
	return render(request, 'core_app/login.html', {'loginf': form })


# View para cerrar la sesión de usuarios
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


#View para editar perfil de cliente
def profile_view(request):
	if request.method == 'POST':	
		if(request.user.profile.is_team_member):
			euf = EditUserForm(request.POST, instance = request.user, prefix='edituser')
			etmf = EditTeamMemberForm(request.POST,request.FILES , instance = request.user.profile, prefix='editmember')
			if etmf.is_valid() * euf.is_valid():
				etmf.save()
				euf.save()			
			return HttpResponseRedirect('/')
		else:
			euf = EditUserForm(request.POST, instance = request.user, prefix='edituser')
			ecpf = EditClientProfileForm(request.POST, instance = request.user.profile, prefix='editprofile')
			if ecpf.is_valid() * euf.is_valid():
				ecpf.save()
				euf.save()			
			return HttpResponseRedirect('/')		
	else:
		euf = EditUserForm(instance = request.user ,prefix='edituser')
		if(request.user.profile.is_team_member):
			etmf = EditTeamMemberForm(instance = request.user.profile, prefix = 'editmember')
			return render(request, 'core_app/editprofile.html', {'editteammemberform':etmf, 'edituserform':euf})
		else:	
			ecpf = EditClientProfileForm(instance = request.user.profile,prefix='editprofile')		
			return render(request, 'core_app/editprofile.html', {'editclientprofileform':ecpf, 'edituserform':euf})#Editar direccion HTML