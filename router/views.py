from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required
def redirect_after_login(request):
    # Create the user groups if does not exist
    Group.objects.get_or_create(name="Doner")
    Group.objects.get_or_create(name="Supervisor")

    user = request.user
    if user.is_authenticated and user.is_active and user.is_staff:
        if user.is_superuser:
            return redirect('/manager/home')
        # elif hasattr(user, 'user_type') and user.user_type == 'student':
        #     return redirect('/student_dashboard/')
        # elif hasattr(user, 'user_type') and user.user_type == 'teacher':
        #     return redirect('/teacher_dashboard/')
        elif user.groups.filter(name='Supervisor').exists():
            return redirect('/supervisor/home')
        elif user.groups.filter(name='Doner').exists():
            return redirect('/doner/home')
        # else:
        #     return redirect('/supervisor/home')
    return redirect('/')  # Default redirect
