# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from decouple import config
#from core_app.forms import RegisterUserForm, LoginForm, EditUserForm, EditClientProfileForm, EditTeamMemberForm, ChangePassForm, DefinePassForm, ContactForm, RecoverPassForm
import core_app.forms as core_forms
from core_app.models import Skill, Profile
from projects_app.models import Project
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import unlock_account_token
from django.views import View
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

	#Le pasamos el formulario de contacto
	contact_f = core_forms.ContactForm()
	context['contact_f'] = contact_f

	return render(request,'core_app/index.html', context)


# View para desplegar el formulario de registro de usuarios y atender las peticiones de registro
def register_view(request):
	if request.method == 'POST':
		ruf = core_forms.RegisterUserForm(request.POST)
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
			return render(request,'core_app/register.html', {'registeruserform':ruf, })
	else:
		ruf = core_forms.RegisterUserForm()
			#Si un usuario con sesión iniciada llega a esta página, se le cerrará la sesión.
		if request.user.is_authenticated:
			logout(request)

		return render(request, 'core_app/register.html', {'registeruserform':ruf,})


# View para autenticar usuarios e iniciar sesión
def login_view(request):
	
	form = core_forms.LoginForm(request.POST or None)

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
			euf = core_forms.EditUserForm(request.POST, instance = request.user, prefix='edituser')
			etmf = core_forms.EditTeamMemberForm(request.POST,request.FILES , instance = request.user.profile, prefix='editmember')
			if etmf.is_valid() * euf.is_valid():
				etmf.save()
				euf.save()			
			return HttpResponseRedirect('/')
		else:
			euf = core_forms.EditUserForm(request.POST, instance = request.user, prefix='edituser')
			ecpf = core_forms.EditClientProfileForm(request.POST, instance = request.user.profile, prefix='editprofile')
			if ecpf.is_valid() * euf.is_valid():
				ecpf.save()
				euf.save()			
			return HttpResponseRedirect('/')		
	else:
		euf = core_forms.EditUserForm(instance = request.user ,prefix='edituser')
		if(request.user.profile.is_team_member):
			etmf = core_forms.EditTeamMemberForm(instance = request.user.profile, prefix = 'editmember')
			return render(request, 'core_app/editprofile.html', {'editteammemberform':etmf, 'edituserform':euf})
		else:	
			ecpf = core_forms.EditClientProfileForm(instance = request.user.profile,prefix='editprofile')		
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
		PasswordForm = core_forms.ChangePassForm
	else:
		PasswordForm = core_forms.DefinePassForm
	
	form = PasswordForm(request.user, request.POST)
	
	if request.method == 'POST' and form.is_valid():
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

def contact_submit(request):
	contact_f = core_forms.ContactForm(request.POST or None)
	if request.method == 'POST' and contact_f.is_valid():
		contact_f.save()
		"""
		Aqui deberiamos enviar 2 correos, uno al que realizo el contacto
		y otro a nuestro propio correo de contacto de la empresa.

		"""
		return redirect('/#contact')
	return redirect('/')

def recoverpassword_view(request):
	form = core_forms.RecoverPassForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		if User.objects.filter(username = form.cleaned_data['user']).exists():
			user = User.objects.get(username = form.cleaned_data['user'])
			if(user.profile.secret_link == form.cleaned_data['secret_link'] ):	
				print(form.cleaned_data['user'])
				link = "/restorepass/" + str(user.id)
				return HttpResponseRedirect(link)
	else:
		form = core_forms.RecoverPassForm()
		return render (request, 'core_app/recoverpass.html', { 'form' : form })

def restorepassword_view(request, pkuser):
	PasswordForm = core_forms.DefinePassForm
	user = User.objects.get(pk=pkuser)
	form = PasswordForm(user , request.POST)	
	if request.method == 'POST' and form.is_valid():
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
		user_profile = Profile.objects.get(user = user)
		user_profile.is_blocked = False
		user_profile.save()
		return HttpResponseRedirect('/')
	else:
		form = PasswordForm(pkuser)
		return render(request, 'core_app/changepassword.html',{'form': form})

def recoversecretlink_view(request):
	form = core_forms.RecoverSecretLinkForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		if User.objects.filter(email = form.cleaned_data['email']).exists():
			user = User.objects.get(email=form.cleaned_data['email'])
			send_mail(
   		 			'Recuperacion de codigo unico',
				    """Hola,
Hemos recibido tu solicitud de recuperación de codigo unico. 
Aqui lo tienes:""" + str(user.profile.secret_link) ,
					config('HOST_USER'),
				    [user.email],
				    fail_silently=False,
					)
			return HttpResponseRedirect('/login')
	else:
		form = core_forms.RecoverSecretLinkForm()
		return render(request, 'core_app/recoversecretlink.html',{'form': form})


class unlockaccount_view(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_unlock_token.check_token(user, token):            
			user.profile.is_blocked = False
			login(request, user)
			form = core_app.DefinePassForm(request.user)
			return render(request,'core_app:restore_pass', {"form" : form })
        else:
            # invalid link
            return render(request, 'registration/invalid.html')