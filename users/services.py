import logging

from django.conf import settings
from django.core.mail import send_mail


def send_activation_email(link, email):
    """
    Формирует и отправляет письмо с подтверждением email для активации пользователя.
    """
    subject = "Дневник. Подтвердите email и можете начать пользоваться"
    message = f"Для подтверждения вашей почты и активации пройдите по ссылке:\n\n{link}"

    if isinstance(email, str):
        email = [email]
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email,
            fail_silently=False,
        )
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка отправки письма: {e}")
        raise
