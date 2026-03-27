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

		category_rows = Categories.objects.values('id', 'name')

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

			category_name = ""
			for category_row in category_rows:
				category_id = category_row["id"]
				if category_id == donation.category_id:
					category_name = category_row["name"]
			output = output + "<td>{}</td>".format(category_name)

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

	def get_category(self, selected_category_id=0):
		output = ""
		output = '<option value="0">Select a category</option>'

		active_categories = Categories.objects.filter(is_active="Y").order_by("name")
		for active_category in active_categories:
			category_id = active_category.id
			category_name = active_category.name
			if category_id == selected_category_id:
				output = output + '<option value="{}" selected>{}</option>'.format(category_id, category_name)
			else:
				output = output + '<option value="{}">{}</option>'.format(category_id, category_name)

		return output

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
		context['category_options'] = self.get_category(0)
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
		category_id = request.POST.get('category_id')
		category_id = int(category_id) if category_id else 0
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

		context['category_id'] = category_id
		context['user_id'] = doner_id
		context['payment_method'] = payment_method
		context['amount'] = amount
		context['service_cost'] = service_cost
		context['notes'] = notes

		context['category_options'] = self.get_category(category_id)
		context['doner_list'] = self.get_doner_list(doner_id)
		context['payment_method_list'] = self.get_payment_method_list(payment_method)

		if category_id < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A category is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif doner_id < 1:
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
					category_id=category_id,
					payment_method=payment_method,
					amount=amount,
					service_cost=service_cost,
					notes=notes,
					added_by=user_id,
					updated_by=user_id,
				)

				context['category_id'] = 0
				context['user_id'] = 0
				context['payment_method'] = ""
				context['amount'] = 0
				context['service_cost'] = 0
				context['notes'] = ""

				context['category_options'] = self.get_category(0)
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

class SupervisorViewCasesPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/view-cases.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "View Cases"
		context['headline'] = "View Cases"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0

		category_rows = Categories.objects.values('id', 'name')

		beneficiary_list = DonationBeneficiaries.objects.filter(is_active="Y").values(
			"id",
			"beneficiary_name",
		)

		donation_case_list = CaseRecords.objects.filter(is_active="Y").order_by("-add_time")
		for donation_case in donation_case_list:
			counter = counter + 1
			case_id = donation_case.id
			output = output + "<tr>"
			output = output + "<td>{}.</td>".format(counter)
			output = output + "<td>{}</td>".format(case_id)
			url = reverse('supervisor:supervisor-case-details', kwargs={'case_id': case_id})
			output = output + '<td><a href="{}" target="_blank">{}</a></td>'.format(url, donation_case.title)

			category_name = ""
			for category_row in category_rows:
				category_id = category_row["id"]
				if category_id == donation_case.category_id:
					category_name = category_row["name"]
			output = output + "<td>{}</td>".format(category_name)

			output = output + "<td>{}</td>".format(donation_case.beneficiary_id)
			beneficiary_list = DonationBeneficiaries.objects.values('id', 'beneficiary_name').order_by("-add_time")
			beneficiary_name = ""
			for beneficiary in beneficiary_list:
				beneficiary_id = beneficiary["id"]

				if donation_case.beneficiary_id == beneficiary_id:
					beneficiary_name = beneficiary["beneficiary_name"]

			output = output + "<td>{}</td>".format(beneficiary_name)
			output = output + "<td>{}</td>".format(donation_case.amount)
			output = output + "<td>{}</td>".format(donation_case.description)
			output = output + "</tr>"
		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorCaseDetailsPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/case-details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Case Details"
		context['headline'] = "Case Details"
		context['output'] = ""
		context['facebook_embed_code'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']

		title = ""
		amount = 0
		category_name = ""
		beneficiary_id = 0
		beneficiary_name = ""
		description = ""
		facebook_embed_code = ""
		case_id = self.kwargs.get('case_id')
		case = CaseRecords.objects.filter(id=case_id).first()
		if case:
			category_rows = Categories.objects.values('id', 'name')

			beneficiary_list = DonationBeneficiaries.objects.filter(is_active="Y").values(
				"id",
				"beneficiary_name",
			)

			title = case.title
			amount = case.amount
			category_id = case.category_id

			category_name = ""
			for category_row in category_rows:
				category_id = category_row["id"]
				if category_id == case.category_id:
					category_name = category_row["name"]

			beneficiary_id = case.beneficiary_id

			for beneficiary in beneficiary_list:
				beneficiary_id = beneficiary["id"]
				if case.beneficiary_id == beneficiary_id:
					beneficiary_name = beneficiary["beneficiary_name"]

			description = case.description
			facebook_embed_code = case.facebook_embed_code

		context['facebook_embed_code'] = facebook_embed_code


		output = output + "<tr>"
		output = output + "<td>Case ID</td>"
		output = output + "<td>{}</td>".format(case_id)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Title</td>"
		output = output + "<td>{}</td>".format(title)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Amount</td>"
		output = output + "<td>{} BDT</td>".format(amount)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Category</td>"
		output = output + "<td>{}</td>".format(category_name)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Beneficiary ID</td>"
		output = output + "<td>{}</td>".format(beneficiary_id)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Beneficiary Name</td>"
		output = output + "<td>{}</td>".format(beneficiary_name)
		output = output + "</tr>"
		output = output + "<tr>"
		output = output + "<td>Description</td>"
		output = output + "<td>{}</td>".format(description)
		output = output + "</tr>"

		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorAddCasePageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/add-case.html'

	def get_beneficiary_list(self, selected_beneficiary_id=0):
		output = ""
		output = '<option value="0">Select a beneficiary</option>'

		active_beneficiaries = DonationBeneficiaries.objects.filter(is_active="Y").order_by("beneficiary_name")
		for active_beneficiary in active_beneficiaries:
			beneficiary_id = active_beneficiary.id
			beneficiary_name = active_beneficiary.beneficiary_name
			if beneficiary_id == selected_beneficiary_id:
				output = output + '<option value="{}" selected>{} - {}</option>'.format(beneficiary_id, beneficiary_id, beneficiary_name)
			else:
				output = output + '<option value="{}">{} - {}</option>'.format(beneficiary_id, beneficiary_id, beneficiary_name)

		return output

	def get_category_list(self, selected_category_id=0):
		output = ""
		output = '<option value="0">Select a category</option>'

		active_categories = Categories.objects.filter(is_active="Y").order_by("name")
		for active_category in active_categories:
			category_id = active_category.id
			category_name = active_category.name
			if category_id == selected_category_id:
				output = output + '<option value="{}" selected>{}</option>'.format(category_id, category_name)
			else:
				output = output + '<option value="{}">{}</option>'.format(category_id, category_name)

		return output

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add Case"
		context['headline'] = "Add Case"
		context['beneficiary_list'] = self.get_beneficiary_list(0)
		context['category_options'] = self.get_category_list(0)
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		beneficiary_id = request.POST.get('beneficiary_id')
		beneficiary_id = int(beneficiary_id) if beneficiary_id else 0
		category_id = request.POST.get('category_id')
		category_id = int(category_id) if category_id else 0
		amount = request.POST.get('amount')
		amount = float(amount) if amount else 0
		case_title = request.POST.get('case_title')
		case_title = str(case_title).strip()
		description = request.POST.get('description')
		description = str(description).strip()
		facebook_embed_code = request.POST.get('facebook_embed_code')
		facebook_embed_code = str(facebook_embed_code).strip()

		context['beneficiary_id'] = beneficiary_id
		context['category_id'] = category_id
		context['amount'] = amount
		context['case_title'] = case_title
		context['description'] = description
		context['facebook_embed_code'] = facebook_embed_code

		context['beneficiary_list'] = self.get_beneficiary_list(beneficiary_id)
		context['category_options'] = self.get_category_list(category_id)

		if beneficiary_id < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A beneficiary is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif category_id < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A category is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif amount <= 0:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The donation amount ({}) is invalid.'.format(amount)
			output = output + '</div>'
			output = output + '</div>'
		elif not case_title:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The title is empty.'
			output = output + '</div>'
			output = output + '</div>'
		elif not facebook_embed_code:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The facebook embed code is empty.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			try:
				user_id = request.user.id
				# Attempt to create the record
				CaseRecords.objects.create(
					beneficiary_id=beneficiary_id,
					category_id=category_id,
					sub_category_id=0,
					amount=amount,
					title=case_title,
					description=description,
					facebook_embed_code=facebook_embed_code,
					added_by=user_id,
					updated_by=user_id,
				)

				context['beneficiary_id'] = 0
				context['category_id'] = 0
				context['amount'] = 0
				context['case_title'] = ""
				context['description'] = ""
				context['facebook_embed_code'] = ""

				context['beneficiary_list'] = self.get_beneficiary_list(0)
				context['category_options'] = self.get_category_list(0)

				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new case for donation: {}.'.format(amount)
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
	template_name = 'supervisor/delivered-donations.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Delivered Donations"
		context['headline'] = "Delivered Donations"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0

		donation_case_list = CaseRecords.objects.filter(is_active="Y").order_by("-add_time")
		category_rows = Categories.objects.values('id', 'name')

		donation_list = DonationGiven.objects.filter(is_active="Y").order_by("-add_time")
		for donation in donation_list:
			counter = counter + 1
			output = output + "<tr>"
			output = output + "<td>{}.</td>".format(counter)
			output = output + "<td>{}</td>".format(donation.case_id)

			case_title = ""
			category_name = ""
			for donation_case in donation_case_list:
				if donation_case.id == donation.case_id:
					case_title= donation_case.title

				for category_row in category_rows:
					category_id = category_row["id"]
					if category_id == donation_case.category_id:
						category_name = category_row["name"]

			output = output + "<td>{}</td>".format(case_title)

			output = output + "<td>{}</td>".format(category_name)

			# output = output + "<td>{}</td>".format(donation.user_id)
			# doner_name = ""
			# doner_email = ""
			# for doner in doners:
			# 	doner_id = doner["id"]

			# 	if donation.user_id == doner_id:
			# 		first_name = doner["first_name"]
			# 		last_name = doner["last_name"]
			# 		doner_email = doner["email"]
			# 		doner_name = "{} {}".format(first_name, last_name)

			# output = output + "<td>{}</td>".format(doner_name)
			# output = output + "<td>{}</td>".format(doner_email)
			output = output + "<td>{}</td>".format(donation.amount)
			output = output + "<td>{}</td>".format(donation.notes)
			output = output + "</tr>"
		context['output'] = output
		return render(request, self.template_name, context)

class SupervisorDeliverDonationPageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/deliver-donation.html'

	def get_case_list(self, selected_case_id=0):
		output = ""
		output = '<option value="0">Select a case</option>'

		# category_rows = Categories.objects.values('id', 'name')

		beneficiary_list = DonationBeneficiaries.objects.values(
			"id",
			"beneficiary_name",
		)

		donation_case_list = CaseRecords.objects.all()

		beneficiary_case_list = CaseRecords.objects.filter(is_active="Y").order_by("-add_time")
		for beneficiary_case in beneficiary_case_list:
			case_id = beneficiary_case.id
			beneficiary_id = beneficiary_case.beneficiary_id
			category_id = beneficiary_case.category_id
			amount = beneficiary_case.amount

			donation_title = ""
			for donation_case in donation_case_list:
				if donation_case.id == case_id:
					donation_title = donation_case.title

			beneficiary_name = ""
			for beneficiary in beneficiary_list:
				if beneficiary["id"] == beneficiary_id:
					beneficiary_name = beneficiary["beneficiary_name"]

			if case_id == selected_case_id:
				output = output + '<option value="{}" selected>Case # {} - {} - {} - {} BDT</option>'.format(case_id, case_id, donation_title, beneficiary_name, amount)
			else:
				output = output + '<option value="{}">Case # {} - {} - {} - {} BDT</option>'.format(case_id, case_id, donation_title, beneficiary_name, amount)

		return output

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Deliver Donation"
		context['headline'] = "Deliver Donation"
		context['case_list'] = self.get_case_list(0)
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		case_id = request.POST.get('case_id')
		case_id = int(case_id) if case_id else 0
		amount = request.POST.get('amount')
		amount = float(amount) if amount else 0
		notes = request.POST.get('notes')
		notes = str(notes).strip()

		context['case_id'] = case_id
		context['amount'] = amount
		context['notes'] = notes

		context['case_list'] = self.get_case_list(case_id)

		if case_id < 1:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> A case is not selected.'
			output = output + '</div>'
			output = output + '</div>'
		elif amount <= 0:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The donation amount ({}) is invalid.'.format(amount)
			output = output + '</div>'
			output = output + '</div>'
		else:
			try:
				user_id = request.user.id
				# Attempt to create the record
				DonationGiven.objects.create(
					case_id=case_id,
					amount=amount,
					notes=notes,
					added_by=user_id,
					updated_by=user_id,
				)

				context['case_id'] = 0
				context['amount'] = 0
				context['notes'] = ""

				context['case_list'] = self.get_case_list(0)

				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new donation grant: {}.'.format(amount)
				output = output + '</div>'
				output = output + '</div>'
			except Exception as e:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Donation grant could not be created.'
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)
