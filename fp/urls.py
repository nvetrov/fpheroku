from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/defender/', include('defender.urls')),  # defender admin
    path('accounts/', include('accounts.urls')),
    # path('admin/', include(admin.site.urls)),  # normal admin

    path('admin/', admin.site.urls),
    path('', include('Products.urls')),

    # -------------------------------------------------------------------------------------------------------------
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('accounts/login/', LoginView.as_view(), name='login'),
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_URL)
