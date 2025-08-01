import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """
    Кастомная модель пользователя, наследуемая от AbstractUser.
    Используется для расширения стандартной модели пользователя Django.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя пользователя",
        help_text="Обязательное поле. Придумайте себе имя пользователя",)
    email = models.EmailField(
        max_length=250,
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Обязательное поле. Введите действительный адрес электронной почты.",
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Можете загрузить свою фотографию профиля.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]


class EmailConfirmation(models.Model):
    """
    Model to store email confirmation tokens.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_confirmations")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email confirmation data for {self.user.email} "

    def is_valid(self) -> bool:
        """
        Проверяет валидность токена.
        :return: True, если токен действителен, иначе False.
        """
        expiration_time = self.created_at + timedelta(days=1)
        return timezone.now() < expiration_time

    @classmethod
    def create_token(cls, user: User) -> "EmailConfirmation":
        """
        Создает новый токен подтверждения электронной почты для пользователя.
        :param user: Пользователь, для которого создается токен.
        :return: Экземпляр EmailConfirmation с новым токеном.
        """
        token = secrets.token_urlsafe(16)
        return cls.objects.create(user=user, token=token)

    class Meta:
        verbose_name = "Подтверждение электронной почты"
        verbose_name_plural = "Подтверждения электронной почты"

