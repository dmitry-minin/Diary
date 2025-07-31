from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import User, EmailConfirmation
from .forms import RegistrationForm
from .services import send_activation_email


class UserRegisterView(CreateView):
    """
    Вью для регистрации пользователя.
    Создаёт неактивного пользователя, отправляет письмо с подтверждением email.
    """
    model = User
    form_class = RegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:please_confirm')

    def form_valid(self, form):
        # создаём неактивного пользователя
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        activation = EmailConfirmation.create_token(user)

        link = self.request.build_absolute_uri(
            reverse_lazy("users:activate", args=[activation.token])
        )
        print(user.email)
        send_activation_email(link, user.email)

        return super().form_valid(form)


class PleaseConfirmView(TemplateView):
    """
    Вью для подтверждения email
    """
    template_name = 'users/please_confirm.html'


class ActivateView(TemplateView):
    """
    Вью для активации пользователя
    """

    template_name = "users/activation_invalid.html"

    def get(self, request, token, *args, **kwargs):
        try:
            activation = EmailConfirmation.objects.get(token=token)
        except EmailConfirmation.DoesNotExist:
            return super().get(request, *args, **kwargs)

        if not activation.is_valid():
            return super().get(request, *args, **kwargs)

        user = activation.user
        user.is_active = True
        user.save(update_fields=["is_active"])

        login(request, user)
        return redirect("diary:home")
