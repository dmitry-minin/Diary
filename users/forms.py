from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя по email и паролю."""

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-white text-dark',
                'style': 'background-color: white !important;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-white text-dark',
                'style': 'background-color: white !important;'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control bg-white text-dark',
                'style': 'background-color: white !important;'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control bg-white text-dark',
                'style': 'background-color: white !important;'
            }),
        }