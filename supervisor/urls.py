from django.urls import path
from .views import HomePageView

app_name = "supervisor"  # optional but recommended
# <a href="{% url 'supervisor:home' %}">Back to Home</a>
# <a href="{% url 'supervisor:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
	# path('', HomePageView.as_view(), name='home'),
]