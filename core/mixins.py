from django.contrib.auth.mixins import UserPassesTestMixin

class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user accessing the view has 'is_superuser=True'.
    """
    def test_func(self):
        # Checks if the user is authenticated and has the is_superuser flag set to True
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    # Optional: Define the URL to redirect to if the test fails
    # If not defined, it defaults to the LOGIN_URL or raises 403 (depending on settings)
    # login_url = '/access-denied/' 
    # raise_exception = True # Raises 403 Forbidden instead of redirecting

class SupervisorRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user accessing the view has 'is_staff=True'.
    """
    def test_func(self):
        # Checks if the user is authenticated AND has the is_staff flag set to True
        # return self.request.user.is_authenticated and self.request.user.is_staff
        return self.request.user.is_authenticated and self.request.user.is_staff and not self.request.user.is_superuser and self.request.user.groups.filter(name='Supervisor').exists()
    
class DonerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user accessing the view has 'is_staff=True'.
    """
    def test_func(self):
        # Checks if the user is authenticated AND has the is_staff flag set to True
        # return self.request.user.is_authenticated and self.request.user.is_staff
        return self.request.user.is_authenticated and self.request.user.is_staff and not self.request.user.is_superuser and self.request.user.groups.filter(name='Doner').exists()
    
