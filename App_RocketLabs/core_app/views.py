# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterUserForm, LoginForm, EditUserForm, EditClientProfileForm, EditTeamMemberForm, ChangePassForm

from projects_app.models import Project
from core_app.models import Skill, Profile

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


# View para desplegar el formulario de registro de usuarios y atender las peticiones de registro
def register_view(request):
	if request.method == 'POST':
		ruf = RegisterUserForm(request.POST)
		if ruf.is_valid():
			user = ruf.save()

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



def allteammember_view(request):
	"""
	Esta view le pasa a la template todos los objetos User
	que sean teammembers y esten activos en el sistema.
	"""
	atm = User.objects.filter(profile__is_team_member = True, is_active=True)
	return render(request, 'core_app/team.html', {'teammember': atm} )

def detailsteammember_view (request, teammember_pk):
	"""
	Esta view le pasa a la template el objeto User indicado con sus habilidades
	y si no es teammember, no esta activo o no existe se retorna un error 404.
	"""
	tm = get_object_or_404(User, is_active=True, profile__is_team_member = True ,pk = teammember_pk)
	return render(request, 'core_app/teammemberdetail.html', {'teammember': tm})


def changepassword_view(request):
	if request.user.has_usable_password():
		PasswordForm = ChangePassForm
	#else:
		#PasswordForm = DefinirPassForm

	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			"""
				#Envio de email con las nuevas credenciales al correo electrónico del usuario
			user = User.objects.get(pk=request.user.id)
			user_profile = Perfil.objects.get(user = user)
			context = {'username': user.username ,'password':form.cleaned_data['new_password1']}
			
			msg_plain = render_to_string('registration/user_pwdreset_email.txt', context)
			msg_html = render_to_string('registration/user_pwdreset_email.html', context)
			
			send_mail(
					'Cambio de Contraseña - Foro-Estudiantil!', #titulo
					msg_plain,									#mensaje txt
					'foroestudiantil2@gmail.com',				#email de envio
					[user.email],								#destinatario
					html_message=msg_html,						#mensaje en html
					)
			"""
				# Nos aseguramos siempre de desbloquar a un usuario despues de el cambio de contraseña
			user = User.objects.get(pk=request.user.id)
			user_profile = Profile.objects.get(user = user)
			user_profile.is_blocked = False
			user_profile.save()
			return HttpResponseRedirect('/')
	else:
		form = PasswordForm(request.user)
		return render(request, 'core_app/changepassword.html',{'form': form})
