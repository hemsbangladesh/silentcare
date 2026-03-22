from django.urls import path
from .views import *

app_name = "manager"  # optional but recommended
# <a href="{% url 'manager:home' %}">Back to Home</a>
# <a href="{% url 'manager:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
	path('manager/home', ManagerHomePageView.as_view(), name='manager-home'),
    path('manager/categories-subcategories', ManagerViewCategoriesSubcategoriesPageView.as_view(), name='manager-categories-subcategories'),
    path('manager/create-category', ManagerCreateCategoryPageView.as_view(), name='manager-create-category'),
    path('manager/edit-category/<int:category_id>', ManagerEditCategoryPageView.as_view(), name='manager-edit-category'),
    path('manager/create-sub-category', ManagerCreateSubCategoryPageView.as_view(), name='manager-create-sub-category'),
]