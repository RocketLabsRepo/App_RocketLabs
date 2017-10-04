# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from decouple import config
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode, is_safe_url
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters

import core_app.forms as core_forms
from core_app.tokens import unlock_account_token
from core_app.models import Skill, Profile
from projects_app.models import Project

# Create your views here.

# Helper function: Yields a generator with objects in l grouped in groups of n.
def grouped(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def home(request):
	context = {}

	# Añadir 4 miembros mas viejos del equipo al contexto.
	four_team_members = User.objects.filter(profile__is_team_member=True, is_active=True).order_by('date_joined')
	four_team_members = four_team_members[:4]
	context['team_members'] = four_team_members
	# Añadir los ultimos 4 proyectos completados al contexto.
	latests_4projects = Project.objects.filter(is_complete = True).order_by('-finish_date')
	latests_4projects = latests_4projects[:4]
	context['latests_projects'] = latests_4projects

	# Añadir todas las habilidades manejadas por la empresa al contexto.
	skills = grouped(Skill.objects.all() , 4)
	context['skill_list'] = skills

	# Añadir el formulario de contacto al contexto.
	contact_form = core_forms.ContactForm()
	context['contact_f'] = contact_form

	return render(request,'core_app/index.html', context)


# View para desplegar el formulario de registro de usuarios y atender las peticiones de registro
def register_view(request):
	if request.method == 'POST':
		ruf = core_forms.RegisterUserForm(request.POST)
		if ruf.is_valid():
			user = ruf.save()
			# Ahora una vez creado el usuario y su perfil procederemos a enviarle un mensaje
			# al email indicado con sus credenciales.
			
			
			context = {'username':ruf.cleaned_data['username'] ,'password':ruf.cleaned_data['password1'], 'secret_link':user.profile.secret_link}
			
			msg_plain = render_to_string('core_app/mail/register_email.txt', context)
			msg_html = render_to_string('core_app/mail/register_email.html', context)
			
			send_mail(
					'Bienvenido a RocketLabs!', 		#titulo
					msg_plain,							#mensaje txt
					config('HOST_USER'),				#email de envio
					[user.email],						#destinatario
					html_message=msg_html,				#mensaje en html
					)
			
			
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
@sensitive_post_parameters()
def login_view(request):
	
	form = core_forms.LoginForm(request.POST or None)

	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			# Si existe alguna url en el parametro 'next' de la petición, nos aseguramos
			# que sea segura y redireccionamos a ella, sino desplegamos el home.
			next_url = request.GET.get('next')
			next_url_is_safe = is_safe_url(
				url=next_url,
				allowed_hosts=request.get_host(),
			)
			return redirect(next_url) if next_url_is_safe else redirect('core_app:home')

	return render(request, 'core_app/login.html', {'loginf': form })


# View para cerrar la sesión de usuarios
@login_required
def logout_view(request):
	logout(request)
	return redirect('core_app:home')


#View para editar perfil de cliente
@login_required
def profile_view(request):
	context={}
	if request.method == 'POST':	
		if(request.user.profile.is_team_member):
			euf = core_forms.EditUserForm(request.POST, instance = request.user, prefix='edituser')
			etmf = core_forms.EditTeamMemberForm(request.POST,request.FILES , instance = request.user.profile, prefix='editmember')
			if etmf.is_valid() * euf.is_valid():
				etmf.save()
				euf.save()
				messages.success(request, 'Sus cambios al perfil han sido guardados con éxito.')
			return redirect('core_app:edit_profile')
		else:
			euf = core_forms.EditUserForm(request.POST, instance = request.user, prefix='edituser')
			ecpf = core_forms.EditClientProfileForm(request.POST, instance = request.user.profile, prefix='editprofile')
			if ecpf.is_valid() * euf.is_valid():
				ecpf.save()
				euf.save()
				messages.success(request, 'Sus cambios al perfil han sido guardados con éxito.')
			return redirect('core_app:edit_profile')
	else:
		user_form = core_forms.EditUserForm(instance = request.user ,prefix='edituser')
		context['user_form'] = user_form

		if(request.user.profile.is_team_member):
		# Si el usuario es un miembro del equipo: 
			member_profile_form = core_forms.EditTeamMemberForm(instance = request.user.profile, prefix = 'editmember')
			context['member_form'] = member_profile_form
			return render(request, 'core_app/editprofile.html', context )
		else:
		# Si el usuario es un cliente:
			client_profile_form = core_forms.EditClientProfileForm(instance = request.user.profile,prefix='editprofile')
			context['client_form'] = client_profile_form
			projects = request.user.profile.project_set.all()
			completed = projects.filter(is_complete=True)
			in_progress = projects.filter(is_complete=False)
			context['completed_projects'] = completed
			context['in_progress_projects'] = in_progress
			return render(request, 'core_app/editprofile.html', context )



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
	estas agrupadas en grupos de 4 y si el User no es teammember, no esta activo
	o no existe se retorna un error 404.
	"""
	context = {}
	tm = get_object_or_404(User, is_active=True, profile__is_team_member = True ,pk = teammember_pk)
	context['teammember'] = tm
	context['known_skills'] = grouped(tm.knows_set.all() , 4)
	return render(request, 'core_app/teammemberdetail.html', context)

@sensitive_post_parameters()
@login_required
def changepassword_view(request):
	if request.user.has_usable_password():
		PasswordForm = core_forms.ChangePassForm
	else:
		PasswordForm = core_forms.DefinePassForm

	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			
			#Envio de email con las nuevas credenciales al correo electrónico del usuario
			user = User.objects.get(pk=request.user.id)
			context = {'username': user.username ,'password':form.cleaned_data['new_password1']}

			msg_plain = render_to_string('core_app/mail/change_password_email.txt', context)
			msg_html = render_to_string('core_app/mail/change_password_email.html', context)

			send_mail(
					'Cambio de Contraseña - Rocket Labs!', 		#titulo
					msg_plain,									#mensaje txt
					config('HOST_USER'),						#email de envio
					[user.email],								#destinatario
					html_message=msg_html,						#mensaje en html
					)		
			
			# Nos aseguramos siempre de desbloquar a un usuario despues de el cambio de contraseña
			user = User.objects.get(pk=request.user.id)
			user_profile = Profile.objects.get(user = user)
			user_profile.is_blocked = False
			user_profile.save()
			messages.success(request, 'Se ha cambiado su contraseña con éxito')
			return redirect('core_app:edit_profile')
		else:
			return render(request, 'core_app/changepassword.html',{'form': form})
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
	return redirect('core_app:home')

@sensitive_post_parameters()
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

@sensitive_post_parameters()
def restorepassword_view(request, pkuser):
	PasswordForm = core_forms.DefinePassForm
	user = User.objects.get(pk=pkuser)		
	if request.method == 'POST' and form.is_valid():
		form = PasswordForm(user , request.POST)
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
		return redirect('core_app:home')
	else:
		form = PasswordForm(pkuser)
		return render(request, 'core_app/changepassword.html',{'form': form})

@sensitive_post_parameters()
def recoversecretlink_view(request):
	form = core_forms.RecoverSecretLinkForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		if User.objects.filter(email = form.cleaned_data['email']).exists():
			user = User.objects.get(email=form.cleaned_data['email'])
			context = {'secret_link':user.profile.secret_link}

			msg_plain = render_to_string('core_app/mail/recover_secret_link_email.txt', context)
			msg_html = render_to_string('core_app/mail/recover_secret_link_email.html', context)

			send_mail(
					'Recuperación de código único - Rocket Labs!', 		#titulo
					msg_plain,											#mensaje txt
					config('HOST_USER'),								#email de envio
					[user.email],										#destinatario
					html_message=msg_html,								#mensaje en html
					)		
			return redirect('core_app:login')
	else:
		form = core_forms.RecoverSecretLinkForm()
		return render(request, 'core_app/recoversecretlink.html',{'form': form})

#3 view para desbloquear usuario
#1. Para tomar email, generar token y enviarlo al email (Verificando si esta bloqueado el usuario o no)
#2. Se le notifica siempre al usuario que se le ha enviado el email
#3. Se hace el desbloqueo de usuario y se le direcciona para que establezca su nueva contraseña

@sensitive_post_parameters()
def unlockuser_view(request):
	form = core_forms.RecoverSecretLinkForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		if User.objects.filter(email = form.cleaned_data['email']).exists():
			user = User.objects.get(email= form.cleaned_data['email'])
			if(user.profile.is_blocked):
				token = unlock_account_token.make_token(user)
				uid = urlsafe_base64_encode(force_bytes(user.pk))
				send_mail(
	   		 			'Desbloquear Cuenta',
					    """Hola,
	Hemos recibido tu solicitud para desbloquear cuenta. 
	Aqui lo tienes: http://localhost:8000/unlockaccount/""" + str(uid) + "/" + str(token),
						config('HOST_USER'),
					    [user.email],
					    fail_silently=False,
						)
				return redirect('core_app:unlockaccount_confirm')
			else:
				return redirect('core_app:unlockaccount_confirm')
		else:
			return redirect('core_app:unlockaccount_confirm')
	else:
		form = core_forms.RecoverSecretLinkForm()
		return render(request, 'core_app/unlockaccount.html',{'form': form})

def unlockaccountconfirm_view(request):
	return render(request,'core_app/unlockaccount_confirm.html')



class unlockaccount_view(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and unlock_account_token.check_token(user, token):            
			user.profile.is_blocked = False
			return HttpResponseRedirect('/restorepass/'+str(user.id))
        else:
            # invalid link
            return render(request, 'core_app/index.html')


###############################################################################################################################################
#ChangeEmail
@sensitive_post_parameters()
@login_required
def changeemail_view(request):

	if request.method == 'POST' :
		form = core_forms.ChangeEmailForm(request.POST or None)
		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			user.email = form.cleaned_data['email']
			user.save()
			messages.success(request, 'Cambio del correo de su cuenta exitoso')
			return redirect('core_app:edit_profile')
		else:
			return render (request, 'core_app/editemail.html', { 'form' : form })
	else:
		form = core_forms.ChangeEmailForm()
		return render (request, 'core_app/editemail.html', { 'form' : form })