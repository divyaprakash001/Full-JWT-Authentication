from django.urls import path,include
from . import views

urlpatterns = [
    path("register/",views.UserRegistrationView.as_view(),name='register'),
    path("login/",views.UserLoginView.as_view(),name='login'),
    path("profile/",views.UserProfileView.as_view(),name='profile'),
    path("change-password/",views.UserChangePasswordView.as_view(),name='changePassword'),
    path("send-reset-password-email/",views.SendPasswordPasswordEmailView.as_view(),name='sendResetPasswordEmail'),
    path("reset-password/<uid>/<token>/",views.UserPasswordResetView.as_view(),name='resetPassword'),
]
