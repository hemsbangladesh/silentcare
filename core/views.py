from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import *

class CoreCategoriesPageView(TemplateView):
	template_name = 'output.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Categories"
		context['headline'] = "Categories"
		context['output'] = ""
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		output = context['output']
		counter = 0
		active_categories = Categories.objects.filter(is_active="Y").order_by("name")
		for active_category in active_categories:
			counter = counter + 1
			category = str(active_category.name).strip()
			output = output + '<p>{}. {}</p>'.format(counter, category)

		context['output'] = output
		return render(request, self.template_name, context)
