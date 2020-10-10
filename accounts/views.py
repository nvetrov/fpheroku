from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect


class ELoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        # print('form_valid')
        return HttpResponseRedirect(self.get_success_url())

