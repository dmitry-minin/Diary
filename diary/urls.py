from django.urls import path
from diary.apps import DiaryConfig
from diary.views import HomeView, DiaryCreateView, DiaryUpdateView, DiaryListView, DiaryDetailView, DiaryDeleteView, \
    NotesCreateView, NotesUpdateView, NotesListView, NotesDetailView, NotesDeleteView

app_name = DiaryConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    path("diary/create/", DiaryCreateView.as_view(), name="create_diary"),
    path("diary/<int:pk>/update/", DiaryUpdateView.as_view(), name="diary_update"),
    path("diary/list/", DiaryListView.as_view(), name="diary_list"),
    path("diary/<int:pk>/", DiaryDetailView.as_view(), name="diary_detail"),
    path("diary/<int:pk>/delete/", DiaryDeleteView.as_view(), name="diary_delete"),

    path("notes/create/", NotesCreateView.as_view(), name="note_create"),
    path("notes/<int:pk>/update/", NotesUpdateView.as_view(), name="note_update"),
    path("notes/list/", NotesListView.as_view(), name="notes_list"),
    path("notes/<int:pk>/", NotesDetailView.as_view(), name="note_detail"),
    path("notes/<int:pk>/delete/", NotesDeleteView.as_view(), name="note_delete"),
]
