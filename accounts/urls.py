from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
# app_name = 'accounts'
from accounts.views import ELoginView

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', ELoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
