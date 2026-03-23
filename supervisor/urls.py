from django.urls import path
from .views import *

app_name = "supervisor"  # optional but recommended
# <a href="{% url 'supervisor:home' %}">Back to Home</a>
# <a href="{% url 'supervisor:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
    path('supervisor/home', SupervisorHomePageView.as_view(), name='supervisor-home'),
]