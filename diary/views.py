from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import DiaryForm, NotesForm
from .models import Diary, Notes


class HomeView(TemplateView):
    """
    Вью для обработки запроса на главную страницы дневника.
    В данном вью мы получаем данные из базы данных и передаем их в контекст.
    Проверяем авторизован ли пользователь.
    Обрабатываем запрос на поиск путем добавления параметра в запрос.
    Если пользователь авторизован, то отображаем его дневник,
    иначе отображаем анонимного пользователя.
    """
    template_name = "diary/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if self.request.user.is_authenticated:
            diaries = Diary.objects.filter(user=self.request.user)

            if search_query:
                diaries = diaries.filter(name__icontains=search_query)
                notes = Notes.objects.filter(
                    Q(diary__name__icontains=search_query) |
                    Q(content__icontains=search_query),
                    user=self.request.user
                ).select_related('diary')

                context['notes'] = notes
                context['search_query'] = search_query
                context['search_performed'] = True

            context['diaries'] = diaries.order_by('-created_at')
        else:
            context['is_anonymous'] = True

        if self.request.user.is_authenticated:
            form = NotesForm()
        else:
            # Создаем форму без поля diary
            form = NotesForm()
            form.fields.pop('diary')

        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('diary:home')
        return self.get(request, *args, **kwargs)


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Вью для создания дневника
    """
    template_name = "diary/create_diary.html"
    form_class = DiaryForm
    model = Diary
    success_url = reverse_lazy("diary:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Вью для обновления дневника
    """
    template_name = "diary/diary_update.html"
    form_class = DiaryForm
    model = Diary
    success_url = reverse_lazy("diary:home")

    def test_func(self):
        """
        Проверка, что пользователь является владельцем дневника
        """
        diary = self.get_object()
        return self.request.user == diary.user


class DiaryListView(LoginRequiredMixin, ListView):
    """
    Вью для просмотра списка дневников
    """
    template_name = "diary/diary_list.html"
    model = Diary
    context_object_name = "diaries"

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user).order_by('-created_at')


class DiaryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Вью для просмотра дневника.
    Выводит только заметки текущего пользователя относящиеся к дневнику
    """
    template_name = "diary/diary_detail.html"
    model = Diary
    context_object_name = "diary"

    def test_func(self):
        """
        Проверка, что пользователь является владельцем дневника
        """
        diary = self.get_object()
        return self.request.user == diary.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = self.object.notes.all().order_by('-created_at')
        context['diaries'] = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return context


class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Вью для удаления дневника
    """
    template_name = "diary/diary_delete.html"
    model = Diary
    success_url = reverse_lazy("diary:home")

    def test_func(self):
        """
        Проверка, что пользователь является владельцем дневника
        """
        diary = self.get_object()
        return self.request.user == diary.user


class NotesCreateView(LoginRequiredMixin, CreateView):
    """
    Вью для создания заметки
    """
    template_name = "diary/note_create.html"
    form_class = NotesForm
    model = Notes
    success_url = reverse_lazy("diary:home")

    def get_initial(self):
        initial = super().get_initial()
        diary_id = self.request.GET.get('diary')
        if diary_id:
            initial['diary'] = diary_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:diary_detail', kwargs={'pk': self.object.diary.pk})


class NotesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Вью для обновления заметки
    """
    template_name = "diary/note_update.html"
    form_class = NotesForm
    model = Notes

    def test_func(self):
        """
        Проверка, что пользователь является владельцем заметки
        """
        note = self.get_object()
        return self.request.user == note.user

    def get_success_url(self):
        return reverse('diary:note_detail', kwargs={'pk': self.object.pk})


class NotesListView(LoginRequiredMixin, ListView):
    """
    Вью для просмотра списка заметок.
    Выводит только заметки текущего пользователя
    """
    template_name = "diary/notes_list.html"
    model = Notes
    context_object_name = "notes"

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)


class NotesDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Вью для просмотра заметки
    """
    template_name = "diary/note_detail.html"
    model = Notes
    context_object_name = "notes"

    def test_func(self):
        """
        Проверка, что пользователь является владельцем заметки
        """
        note = self.get_object()
        return self.request.user == note.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diaries'] = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return context


class NotesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Вью для удаления заметки
    """
    template_name = "diary/note_delete.html"
    model = Notes
    success_url = reverse_lazy("diary:home")

    def get_queryset(self):
        """
        Возвращает QuerySet заметок, принадлежащих текущему пользователю
        """
        return Notes.objects.filter(user=self.request.user)

    def test_func(self):
        """
        Проверка, что пользователь является владельцем заметки
        """
        note = self.get_object()
        return self.request.user == note.user
