from django.urls import path
from .views import redirect_after_login

urlpatterns = [
    path('redirect-after-login/', redirect_after_login,
         name='redirect-after-login'),
    # ... other paths
]
