from django.urls import path
from .views import *

app_name = "doner"  # optional but recommended
# <a href="{% url 'doner:home' %}">Back to Home</a>
# <a href="{% url 'doner:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
	path('doner/home', DonerHomePageView.as_view(), name='doner-home'),
]