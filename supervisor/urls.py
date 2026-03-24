from django.urls import path
from .views import *

app_name = "supervisor"  # optional but recommended
# <a href="{% url 'supervisor:home' %}">Back to Home</a>
# <a href="{% url 'supervisor:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
    path('supervisor/home', SupervisorHomePageView.as_view(), name='supervisor-home'),
    path('supervisor/view-beneficiaries', SupervisorViewBeneficiariesPageView.as_view(), name='supervisor-view-beneficiaries'),
    path('supervisor/add-beneficiary', SupervisorAddBeneficiaryPageView.as_view(), name='supervisor-add-beneficiary'),
    path('supervisor/view-donations', SupervisorViewDonationsPageView.as_view(), name='supervisor-view-donations'),
    path('supervisor/add-donation', SupervisorAddDonationPageView.as_view(), name='supervisor-add-donation'),
    path('supervisor/delivered-donations', SupervisorDeliveredDonationsPageView.as_view(), name='supervisor-delivered-donations'),
    path('supervisor/deliver-donation', SupervisorDeliverDonationPageView.as_view(), name='supervisor-deliver-donation'),
]