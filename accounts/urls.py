from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


from django.urls import path
from django.contrib.auth import views as auth_views



app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', profile_view, name="profile"),
    path('signup/', signup_view, name="signup"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]



urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)