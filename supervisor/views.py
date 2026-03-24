from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import *
from django.urls import reverse
######################### LOGIN AND USER ACCESS CHECK #########################
from core.mixins import SupervisorRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
######################### LOGIN AND USER ACCESS CHECK #########################
from django.contrib.auth import get_user_model

User = get_user_model()

class SupervisorHomePageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Welcome Admin"
		context['headline'] = "Welcome Admin"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

class SupervisorViewBeneficiariesPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/view-beneficiaries.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "View Beneficiaries"
		context['headline'] = "View Beneficiaries"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0
		donation_beneficiaries = DonationBeneficiaries.objects.filter(is_active="Y").order_by("beneficiary_name")
		for donation_beneficiary in donation_beneficiaries:
			counter = counter + 1
			output = output + "<tr>"
			output = output + "<td>{}.</td>".format(counter)
			output = output + "<td>{}</td>".format(donation_beneficiary.id)
			output = output + "<td>{}</td>".format(donation_beneficiary.beneficiary_name)
			output = output + "<td>{}</td>".format(donation_beneficiary.guardian_name)
			output = output + "<td>{}</td>".format(donation_beneficiary.address)
			output = output + "<td>{}</td>".format(donation_beneficiary.mobile_number)
			output = output + "</tr>"
		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorAddBeneficiaryPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/add-beneficiary.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add sBeneficiary"
		context['headline'] = "Add Beneficiary"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		beneficiary_name = request.POST.get('beneficiary_name')
		beneficiary_name = str(beneficiary_name).strip()
		guardian_name = request.POST.get('guardian_name')
		guardian_name = str(guardian_name).strip()
		address = request.POST.get('address')
		address = str(address).strip()
		mobile_number = request.POST.get('mobile_number')
		mobile_number = str(mobile_number).strip()

		context['beneficiary_name'] = beneficiary_name
		context['guardian_name'] = guardian_name
		context['address'] = address
		context['mobile_number'] = mobile_number

		if not beneficiary_name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The beneficiary name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not guardian_name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The guardian name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not address:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The address is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not mobile_number:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The mobile number is empty.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			user_id = request.user.id
			obj, created = DonationBeneficiaries.objects.get_or_create(
				beneficiary_name=beneficiary_name,
				guardian_name=guardian_name,
				address=address,
				mobile_number=mobile_number,
				defaults={
					'added_by': user_id,
					'updated_by': user_id,
					'is_active': 'Y'
				}
			)

			if created:
				context['beneficiary_name'] = ""
				context['guardian_name'] = ""
				context['address'] = ""
				context['mobile_number'] = ""

				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new beneficiary: {}.'.format(obj.beneficiary_name)
				output = output + '</div>'
				output = output + '</div>'
			else:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Beneficiary ({}) already exists.'.format(obj.beneficiary_name)
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorViewDonationsPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/view-donations.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "View Donations"
		context['headline'] = "View Donations"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0

		doners = User.objects.filter(groups__name="Doner").values(
			"id",
			"first_name",
			"last_name",
			"email",
		)

		donation_list = DonationReceived.objects.filter(is_active="Y").order_by("-add_time")
		for donation in donation_list:
			counter = counter + 1
			output = output + "<tr>"
			output = output + "<td>{}.</td>".format(counter)
			output = output + "<td>{}</td>".format(donation.user_id)

			doner_name = ""
			doner_email = ""
			for doner in doners:
				doner_id = doner["id"]

				if donation.user_id == doner_id:
					first_name = doner["first_name"]
					last_name = doner["last_name"]
					doner_email = doner["email"]
					doner_name = "{} {}".format(first_name, last_name)

			output = output + "<td>{}</td>".format(doner_name)
			output = output + "<td>{}</td>".format(doner_email)
			output = output + "<td>{}</td>".format(donation.amount)
			output = output + "<td>{}</td>".format(donation.service_cost)
			output = output + "<td>{}</td>".format(donation.notes)
			output = output + "</tr>"
		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorAddDonationPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/add-donation.html'

	def get_doner_list(self, selected_doner_id=0):
		output = ""
		output = output + '<option value="0">Select a doner</option>'

		doners = User.objects.filter(groups__name="Doner").values(
			"id",
			"first_name",
			"last_name",
			"email",
		)

		for doner in doners:
			user_id = doner["id"]
			first_name = doner["first_name"]
			last_name = doner["last_name"]
			email = doner["email"]

			if user_id == selected_doner_id:
				output = output + '<option value="{}" selected>{} - {} {} ({})</option>'.format(user_id, user_id, first_name, last_name, email)
			else:
				output = output + '<option value="{}">{} - {} {} ({})</option>'.format(user_id, user_id, first_name, last_name, email)

		return output

	def get_payment_method_list(self, selected_payment_method=''):
		output = ""
		payment_method_list = ["Cash", "Check", "bKash", "Nagad", "Rocket",]

		output = output + '<option value="">Select a payment method</option>'
		for payment_method in payment_method_list:
			payment_method = str(payment_method).strip()
			if payment_method == selected_payment_method:
				output = output + '<option value="{}" selected>{}</option>'.format(payment_method, payment_method)
			else:
				output = output + '<option value="{}">{}</option>'.format(payment_method, payment_method)

		return output

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add Donation"
		context['headline'] = "Add Donation"
		context['doner_list'] = self.get_doner_list(0)
		context['payment_method_list'] = self.get_payment_method_list('')
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		doner_id = request.POST.get('user_id')
		doner_id = int(doner_id) if doner_id else 0
		payment_method = request.POST.get('payment_method')
		payment_method = str(payment_method).strip()
		amount = request.POST.get('amount')
		amount = float(amount) if amount else 0
		service_cost = request.POST.get('service_cost')
		service_cost = float(service_cost) if service_cost else 0
		notes = request.POST.get('notes')
		notes = str(notes).strip()

		context['user_id'] = doner_id
		context['payment_method'] = payment_method
		context['amount'] = amount
		context['service_cost'] = service_cost
		context['notes'] = notes

		context['doner_list'] = self.get_doner_list(doner_id)
		context['payment_method_list'] = self.get_payment_method_list(payment_method)

		if doner_id < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A doner is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif not payment_method:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A payment method is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif amount <= 0:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The donation amount ({}) is invalid.'.format(amount)
			output = output + '</div>'
			output = output + '</div>'
		elif service_cost < 0:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The service cost ({}) is invalid.'.format(service_cost)
			output = output + '</div>'
			output = output + '</div>'
		elif not notes:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The note is empty.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			try:
				user_id = request.user.id
				# Attempt to create the record
				DonationReceived.objects.create(
					user_id=doner_id,
					payment_method=payment_method,
					amount=amount,
					service_cost=service_cost,
					notes=notes,
					added_by=user_id,
					updated_by=user_id,
				)

				context['user_id'] = 0
				context['payment_method'] = ""
				context['amount'] = 0
				context['service_cost'] = 0
				context['notes'] = ""

				context['doner_list'] = self.get_doner_list(0)
				context['payment_method_list'] = self.get_payment_method_list('')

				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new donation: {}.'.format(amount)
				output = output + '</div>'
				output = output + '</div>'
			except Exception as e:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Donation could not be created.'
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorDeliveredDonationsPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Delivered Donations"
		context['headline'] = "Delivered Donations"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

class SupervisorDeliverDonationPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Deliver Donation"
		context['headline'] = "Deliver Donation"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

