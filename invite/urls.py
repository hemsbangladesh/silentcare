from django.urls import path
from .views import *

app_name = "invite"  # optional but recommended
# <a href="{% url 'invite:home' %}">Back to Home</a>
# <a href="{% url 'invite:post_detail' pk=5 %}">Open Post 5</a>

urlpatterns = [
    path('invite/send-invitation-to-join', InviteSendInvitationToJoinPageView.as_view(), name='invite-send-invitation-to-join'),
    path('invite/invite-view-invitation-list', InviteViewInvitationListPageView.as_view(), name='invite-view-invitation-list'),
    path('invite/create-account/<str:secret_code>/<int:invitation_id>', InviteCreateAccountPageView.as_view(), name='invite-create-account'),
]