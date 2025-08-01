from django.contrib import admin
from .models import Diary, Notes


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name", "user__username")
    ordering = ("created_at",)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("user", "diary", "title", "event_date", "image", "created_at", "updated_at")
    list_filter = ("created_at", "event_date", "diary", "user")
    search_fields = ("title", "content", "user__username")
    ordering = ("created_at",)
