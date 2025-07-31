from users.apps import UsersConfig
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

from users.views import UserRegisterView, ActivateView, PleaseConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path("please-confirm/", PleaseConfirmView.as_view(), name="please_confirm"),
    path('activate/<str:token>/', ActivateView.as_view(), name='activate'),

    path("login/", LoginView.as_view(
        template_name="users/login.html"
    ), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("password_reset/", PasswordResetView.as_view(
        template_name="users/password_reset.html",
        email_template_name="users/password_reset_email.html",
        success_url=reverse_lazy("users:password_reset_done")
    ), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")
    ), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"
    ), name="password_reset_complete"),

]
