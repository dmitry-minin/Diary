from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from .models import Diary, Notes


class DiaryForm(forms.ModelForm):
    """
    Форма для создания дневника
    """

    class Meta:
        model = Diary
        fields = ["name"]
        labels = {
            "name": "Название дневника",
        }
        help_texts = {
            "name": "Поле обязательно для заполнения",

        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control bg-light text-dark",
                "placeholder": "Введите название дневника"
            })
        }


class NotesForm(forms.ModelForm):
    """
    Форма для создания заметки
    """

    class Meta:
        model = Notes
        fields = ["event_date", "diary", "title", "content", "image"]
        labels = {
            "diary": "Дневник",
            "title": "Название заметки",
            "content": "Текст заметки",
            "event_date": "Дата события",
            "image": "Изображение",
        }
        
        widgets = {
            "diary": forms.Select(attrs={
                "class": "form-select bg-light text-dark",
                "placeholder": "Выберите дневник"},),
            "title": forms.TextInput(attrs={
                "class": "form-control bg-light text-dark",
                "placeholder": "Введите тему или название заметки"},),
            "content": forms.Textarea(attrs={
                "class": "form-control bg-light text-dark",
                "placeholder": "Поле для вашего текста",
                "rows": 4},),
            "event_date": forms.DateInput(attrs={
                "class": "form-control bg-light text-dark",
                "type": "date",
                "placeholder": "Введите дату события"},),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control bg-light text-dark",
                "placeholder": "Можете прикрепить изображение",
                "accept": "image/*"},),
        }

        def clean_image(self):
            """
            Проверка размера изображения 10 МБ
            :return:
            """
            image = self.cleaned_data.get('image')
            if image:

                max_size = 10 * 1024 * 1024
                if image.size > max_size:
                    raise ValidationError(
                        f'Максимальный размер файла {filesizeformat(max_size)}. '
                        f'Ваш файл весит {filesizeformat(image.size)}'
                    )
            return image
