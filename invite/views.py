from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import *
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.conf import settings

class InviteSendInvitationToJoinPageView(TemplateView):
	template_name = 'invite/send-invitation.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Send invitation to join"
		context['headline'] = "Send invitation to join"
		context['user_type'] = ""
		context['output'] = ""

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		user_type = request.POST.get('user_type')
		email = request.POST.get('email')
		context['user_type'] = user_type
		# 32 character random string
		secret_code = get_random_string(length=32)

		if not user_type:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> You did not select a user type.'
			output = output + '</div>'
			output = output + '</div>'
		elif not email:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The email is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not secret_code:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The secret code is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif Invitations.objects.filter(email=email).exists():
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> An invitation for this email ({}) already exists.'.format(email)
			output = output + '</div>'
			output = output + '</div>'
		else:
			user_id = request.user.id
			obj, created = Invitations.objects.get_or_create(
				user_type=user_type,
				email=email,
				secret_code=secret_code,
				defaults={
					'added_by': user_id,
					'updated_by': user_id,
					'is_active': 'Y'
				}
			)

			if created:
				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully invitation created for: {}.'.format(obj.email)
				output = output + '</div>'
				output = output + '</div>'
			else:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Invitation already exists for: {}.'.format(obj.email)
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)

class InviteViewInvitationListPageView(TemplateView):
	template_name = 'invite/invitation-list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "View invitation list"
		context['headline'] = "View invitation list"
		context['user_type'] = ""
		context['output'] = ""
		output = ''

		# invitation_list = Invitations.objects.filter(is_active="Y").order_by("-add_time")
		invitation_list = Invitations.objects.all().order_by("-add_time")
		counter = 0
		for invitation in invitation_list:
			counter = counter + 1
			invitation_id = invitation.id
			user_type = invitation.user_type
			email = invitation.email
			secret_code = invitation.secret_code
			is_active = invitation.is_active
			url = reverse('invite:invite-create-account', kwargs={'secret_code': secret_code, 'invitation_id': invitation_id})
			
			output = output + "<tr>"
			output = output + "<td>{}.</td>".format(counter)
			output = output + "<td>{}</td>".format(str(user_type).title())
			output = output + '<td><a href="mailto:{}">{}</a></td>'.format(email, email)
			if is_active == 'Y':
				output = output + "<td>Yes</td>"
			else:
				output = output + "<td>No</td>"
			output = output + '<td><a href="{}" target="_blank">Invitation link</a></td>'.format(url)
			output = output + "</tr>"

		context['output'] = output
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

class InviteCreateAccountPageView(TemplateView):
	template_name = 'invite/create-account.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Create account"
		context['headline'] = "Create account"
		context['user_type'] = ""
		context['output'] = ""

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		context['email'] = ''
		context['username'] = ''
		context['first_name'] = ''
		context['last_name'] = ''
		context['password'] = ''
		context['confirm_password'] = ''
		context['is_invitation_found'] = False
		context['is_user_found'] = False
		secret_code = kwargs.get('secret_code')
		invitation_id = kwargs.get('invitation_id')
		user_type = ''
		user_email = ''
		invitation = Invitations.objects.filter(id=invitation_id, secret_code=secret_code).first()
		if invitation:
			user_type = invitation.user_type
			user_email = invitation.email
	
		context['user_type'] = user_type
		context['is_invitation_found'] = Invitations.objects.filter(id=invitation_id, secret_code=secret_code).exists()
		context['is_user_found'] = User.objects.filter(email=user_email).exists()

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		context['is_invitation_found'] = False
		context['is_user_found'] = False
		secret_code = kwargs.get('secret_code')
		invitation_id = kwargs.get('invitation_id')
		user_type = ''
		user_email = ''
		invitation = Invitations.objects.filter(id=invitation_id, secret_code=secret_code).first()
		if invitation:
			user_type = invitation.user_type
			user_email = invitation.email
	
		user_type = str(user_type).strip()
		context['user_type'] = user_type
		context['is_invitation_found'] = Invitations.objects.filter(id=invitation_id, secret_code=secret_code).exists()
		context['is_user_found'] = User.objects.filter(email=user_email).exists()

		output = context['output']
		email = request.POST.get('email')
		username = request.POST.get('username')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		context['email'] = email
		context['username'] = username
		context['first_name'] = first_name
		context['last_name'] = last_name
		context['password'] = password
		context['confirm_password'] = confirm_password
		context['user_type'] = user_type

		if not email:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The email is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif email != user_email:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> Your email does not match with our record in database.'
			output = output + '</div>'
			output = output + '</div>'
		elif not first_name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The first name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not last_name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The last name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not user_type:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> Your user type is not found.'
			output = output + '</div>'
			output = output + '</div>'
		elif not password:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The password is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif len(str(password).strip()) < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The password is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif len(str(password).strip()) < 8:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The password must contain at least 8 characters.'
			output = output + '</div>'
			output = output + '</div>'
		elif password != confirm_password:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The password and confirm password do not match.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			group_name = ''
			if user_type == 'admin':
				group_name = 'Supervisor'
			elif user_type == 'doner':
				group_name = 'Doner'

			# Check if user already exists
			if User.objects.filter(username=username).exists():
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> This username ({}) already exists.'.format(username)
				output = output + '</div>'
				output = output + '</div>'
			elif User.objects.filter(email=email).exists():
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> This username ({}) already exists.'.format(username)
				output = output + '</div>'
				output = output + '</div>'
			else:
				# Create user
				user = User.objects.create_user(
					username=username,
					email=email,
					password=password,
					first_name=first_name,
					last_name=last_name,
					is_staff=True # Give user login permission
				)

				# Get or create group
				group, created = Group.objects.get_or_create(name=group_name)
				# Assign user to group
				user.groups.add(group)

				login_url = settings.LOGIN_URL
				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Your account is created. <a href="{}" target="_blank">Click here</a> to login now.'.format(login_url)
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)

