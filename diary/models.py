from django.db import models
from django.conf import settings


class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diaries",
                             verbose_name="Пользователь", help_text="Пользователь, которому принадлежит дневник")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название дневника",
                            help_text="Создай свой дневник")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Дневник"
        verbose_name_plural = "Дневники"


class Notes(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name="notes", verbose_name="Дневник",
                              help_text="Дневник, к которому принадлежит заметка")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заголовок заметки",
                             help_text="Введите заголовок для вашей заметки")
    content = models.TextField(verbose_name="Запись",
                               help_text="Тут вы можете написать свои мысли, события дня или что-то важное")
    image = models.ImageField(upload_to="notes/images/", blank=True, null=True, verbose_name="Изображение",
                              help_text="Можете добавить изображение к заметке", )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания",
                                      help_text="Дата и время создания заметки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления",
                                      help_text="Дата и время последнего обновления заметки")

    def __str__(self):
        return (f"{self.title if self.title else 'Без заголовка'} - Дневник: {self.diary.name} "
                f"({self.created_at.strftime('%Y-%m-%d')})")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
