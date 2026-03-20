from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import *

class ManagerHomePageView(TemplateView):
	template_name = 'manager/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Welcome Super Admin"
		context['headline'] = "Welcome Super Admin"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

class ManagerViewCategoriesSubcategoriesPageView(TemplateView):
	template_name = 'manager/categories-subcategories.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Categories &amp; sub-categories"
		context['headline'] = "Categories &amp; sub-categories"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0
		active_categories = Categories.objects.filter(is_active="Y").order_by("name")
		for active_category in active_categories:
			active_sub_categories = SubCategories.objects.filter(is_active="Y").order_by("name")
			if len(active_sub_categories) > 0:
				for active_sub_category in active_sub_categories:
					counter = counter + 1
					output = output + "<tr>"
					output = output + "<td>{}.</td>".format(counter)
					output = output + "<td>{}</td>".format(active_category.name)
					output = output + "<td>{}</td>".format(active_sub_category.name)
					output = output + "</tr>"
			else:
				counter = counter + 1
				output = output + "<tr>"
				output = output + "<td>{}.</td>".format(counter)
				output = output + "<td>{}</td>".format(active_category.name)
				output = output + "<td>N/A</td>"
				output = output + "</tr>"
		context['output'] = output
		return render(request, self.template_name, context)

class ManagerCreateCategoryPageView(TemplateView):
	template_name = 'manager/create-category.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Create a category"
		context['headline'] = "Create a category"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		name = request.POST.get('name')
		name = str(name).strip()
		if not name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The category name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			user_id = request.user.id
			obj, created = Categories.objects.get_or_create(
				name=name,
				defaults={
					'added_by': user_id,
					'updated_by': user_id,
					'is_active': 'Y'
				}
			)

			if created:
				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new category: {}.'.format(obj.name)
				output = output + '</div>'
				output = output + '</div>'
			else:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Category ({}) already exists.'.format(obj.name)
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)

class ManagerCreateSubCategoryPageView(TemplateView):
	template_name = 'manager/create-sub-category.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Create a sub-category"
		context['headline'] = "Create a sub-category"
		context['output'] = ""

		category_options = '<option value="0">Select a category</option>'

		active_categories = Categories.objects.filter(is_active="Y").order_by("name")
		for active_category in active_categories:
			category_options = category_options + '<option value="{}">{}</option>'.format(active_category.id, active_category.name)

		context['category_options'] = category_options
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		category_id = request.POST.get('category_id')
		category_id = int(category_id)
		name = request.POST.get('name')
		name = str(name).strip()
		if category_id <= 0:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> You did not select a category.'
			output = output + '</div>'
			output = output + '</div>'
		elif not name:
			output = output + '<div>'
			output = output + '<div class="alert alert-danger" role="alert">'
			output = output + '<strong>Oops!</strong> The category name is empty.'
			output = output + '</div>'
			output = output + '</div>'
		else:
			user_id = request.user.id
			obj, created = SubCategories.objects.get_or_create(
				category_id=category_id,
				name=name,
				defaults={
					'added_by': user_id,
					'updated_by': user_id,
					'is_active': 'Y'
				}
			)

			if created:
				output = output + '<div>'
				output = output + '<div class="alert alert-success" role="alert">'
				output = output + '<strong>Good news!</strong> Successfully created new sub-category: {}.'.format(obj.name)
				output = output + '</div>'
				output = output + '</div>'
			else:
				output = output + '<div>'
				output = output + '<div class="alert alert-danger" role="alert">'
				output = output + '<strong>Oops!</strong> Sub-category ({}) already exists.'.format(obj.name)
				output = output + '</div>'
				output = output + '</div>'

		context['output'] = output
		return render(request, self.template_name, context)