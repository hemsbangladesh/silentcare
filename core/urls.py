from django.urls import path
from .views import *

app_name = "core"  # optional but recommended
# <a href="{% url 'core:home' %}">Back to Home</a>
# <a href="{% url 'core:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
    path('core/categories', CoreCategoriesPageView.as_view(), name='core-categories'),
]