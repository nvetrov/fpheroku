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

#https://stackoverflow.com/questions/14808238/middleware-is-not-work-expected/14808426#14808426
# class AutoLogout:
#     def process_request(self, request):
#         if not request.user.is_authenticated() :
#             return HttpResponseRedirect(reverse('app_name:url_name'))
#
#         try:
#             if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
#                 auth.logout(request)
#                 del request.session['last_touch']
#                 return HttpResponseRedirect(reverse('app_name:url_name'))
#         except KeyError:
#             pass
#
#         request.session['last_touch'] = datetime.now()