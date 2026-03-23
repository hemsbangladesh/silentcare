from django.views.generic import TemplateView
######################### LOGIN AND USER ACCESS CHECK #########################
from core.mixins import SupervisorRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
######################### LOGIN AND USER ACCESS CHECK #########################

class SupervisorHomePageView(LoginRequiredMixin, SupervisorRequiredMixin, TemplateView):
	template_name = 'supervisor/home.html'