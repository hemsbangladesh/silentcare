from django.views.generic import TemplateView
######################### LOGIN AND USER ACCESS CHECK #########################
from core.mixins import DonerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
######################### LOGIN AND USER ACCESS CHECK #########################

class DonerHomePageView(LoginRequiredMixin, DonerRequiredMixin, TemplateView):
	template_name = 'doner/home.html'