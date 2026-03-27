from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import *
from django.urls import reverse
######################### LOGIN AND USER ACCESS CHECK #########################
from core.mixins import DonerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
######################### LOGIN AND USER ACCESS CHECK #########################

class DonerHomePageView(LoginRequiredMixin, DonerRequiredMixin, TemplateView):
	template_name = 'doner/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Welcome Doner"
		context['headline'] = "Welcome Doner"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		context['output'] = output
		return render(request, self.template_name, context)

class DonerViewCasesPageView(LoginRequiredMixin, DonerRequiredMixin, TemplateView):
	template_name = 'doner/view-cases.html'

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
			url = reverse('doner:doner-case-details', kwargs={'case_id': case_id})
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

class DonerCaseDetailsPageView(LoginRequiredMixin, DonerRequiredMixin, TemplateView):
	template_name = 'doner/case-details.html'

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
