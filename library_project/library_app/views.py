from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from library_app.models import CustomUser, Book, LoanHistory, Author
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone




# Create your views here.

def loginPage(request):
    """
    Отображение страницы входа.

    :param request: Объект запроса Django.
    :return: Ответ с страницей входа.
    """
    return render(request, 'auth.html')

def login_view(request):
    """
    Обработка запроса на вход пользователя.

    При успешной аутентификации пользователя перенаправляет на страницу списка книг.

    :param request: Объект запроса Django.
    :return: Перенаправление на страницу списка книг или страницу входа с сообщением об ошибке.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('books')  
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    """
    Обработка запроса на регистрацию нового пользователя.

    При успешной регистрации пользователя перенаправляет на страницу входа.

    :param request: Объект запроса Django.
    :return: Перенаправление на страницу входа с сообщением о успешной регистрации или страницу регистрации с формой.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'reader'
            user.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('auth')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})
  
def logout_view(request):
    """
    Обработка запроса на выход пользователя.

    :param request: Объект запроса Django.
    :return: Перенаправление на страницу входа.
    """
    logout(request)
    return redirect('auth')

class BookListView(ListView):
    """
    Отображение списка книг.

    :param ListView: Объект представления списка Django.
    :return: Ответ с шаблоном списка книг.
    """
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        queryset = Book.objects.all()

        filter_param = self.request.GET.get('filter')
        sort_param = self.request.GET.get('sort')

        if filter_param == 'available':
            queryset = queryset.filter(status='available')

        if sort_param:
            queryset = queryset.order_by(sort_param)

        return queryset
    
class BookUpdateView(UpdateView):
    """
    Обновление информации о книге.

    :param UpdateView: Объект представления обновления Django.
    :return: Ответ с формой обновления книги или перенаправление на список книг при успешном обновлении.
    """
    model = Book
    fields = ['title', 'genre', 'author', 'publication_year', 'edition', 'unique_code']
    template_name = 'book_update.html' 
    success_url = reverse_lazy('books')
    
    
class BookDetailView(DetailView):
    """
    Отображение детальной информации о книге.

    :param DetailView: Объект представления детали Django.
    :return: Ответ с шаблоном детальной информации о книге.
    """
    model = Book
    template_name = 'book_detail.html'
      
class BookCreateView(CreateView):
    """
    Создание новой книги.

    :param CreateView: Объект представления создания Django.
    :return: Ответ с формой создания книги или перенаправление на список книг при успешном создании.
    """
    model = Book
    fields = ['title', 'genre', 'author', 'publication_year', 'edition', 'unique_code']
    template_name = 'book_add.html'
    success_url = reverse_lazy('books')
      
def delete_book(request, pk):
    """
    Удаление книги.

    :param request: Объект запроса Django.
    :param pk: Primary key книги для удаления.
    :return: Перенаправление на список книг.
    """
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('books')
  
class HistoryListView(ListView):
    """
    Отображение списка истории книг.

    :param ListView: Объект представления списка Django.
    :return: Ответ с шаблоном списка истории книг.
    """
    model = LoanHistory
    template_name = 'history_list.html'
    context_object_name = 'histories'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'loan_date':
            queryset = queryset.order_by('-loan_date')
        elif sort_by == 'return_date':
            queryset = queryset.order_by('-return_date')
        return queryset
    
class HistoryUpdateView(UpdateView):
    """
    Обновление информации об истории книг.

    :param UpdateView: Объект представления обновления Django.
    :return: Ответ с формой обновления истории книги или перенаправление на список истории при успешном обновлении.
    """
    model = LoanHistory
    fields = ['user', 'book', 'loan_date', 'return_date']
    template_name = 'history_update.html' 
    success_url = reverse_lazy('history_list')
    
class HistoryCreateView(CreateView):
    """
    Создание новой истории книги.

    :param CreateView: Объект представления создания Django.
    :return: Ответ с формой создания истории книги или перенаправление на список истории при успешном создании.
    """
    model = LoanHistory
    fields = ['user', 'book', 'loan_date', 'return_date']
    template_name = 'history_create.html'
    success_url = reverse_lazy('history_list')
    
def history_delete(request, pk):
    """
    Удаление истории книги.

    :param request: Объект запроса Django.
    :param pk: Primary key истории книги для удаления.
    :return: Перенаправление на список истории книг.
    """
    history = get_object_or_404(LoanHistory, id=pk)
    history.delete()
    return redirect('history_list')
  
class AuthorListView(ListView):
    """
    Отображение списка авторов.

    :param ListView: Объект представления списка Django.
    :return: Ответ с шаблоном списка авторов.
    """
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')

        if sort_by == 'first_name':
            queryset = queryset.order_by('first_name')
        elif sort_by == 'last_name':
            queryset = queryset.order_by('last_name')
        elif sort_by == 'date_of_birth':
            queryset = queryset.order_by('date_of_birth')
        elif sort_by == 'date_of_death':
            queryset = queryset.order_by('date_of_death')

        return queryset
    
class AuthorUpdateView(UpdateView):
    """
    Обновление информации об авторе.

    :param UpdateView: Объект представления обновления Django.
    :return: Ответ с формой обновления информации об авторе или перенаправление на список авторов при успешном обновлении.
    """
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']
    template_name = 'author_update.html' 
    success_url = reverse_lazy('author_list')
    
class AuthorCreateView(CreateView):
    """
    Создание нового автора.

    :param CreateView: Объект представления создания Django.
    :return: Ответ с формой создания нового автора или перенаправление на список авторов при успешном создании.
    """
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']
    template_name = 'author_create.html'
    success_url = reverse_lazy('author_list')
    
class AuthorDetailView(DetailView):
    """
    Отображение детальной информации о книге.

    :param DetailView: Объект представления детали Django.
    :return: Ответ с шаблоном детальной информации о книге.
    """
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'
    
def author_delete(request, pk):
    """
    Удаление автора.

    :param request: Объект запроса Django.
    :param pk: Primary key автора для удаления.
    :return: Перенаправление на список авторов.
    """
    author = get_object_or_404(Author, id=pk)
    author.delete()
    return redirect('author_list')
  
class UsersListView(ListView):
    """
    Отображение списка пользователей.

    :param ListView: Объект представления списка Django.
    :return: Ответ с шаблоном списка пользователей.
    """
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserUpdateView(UpdateView):
    """
    Обновление информации о пользователе.

    :param UpdateView: Объект представления обновления Django.
    :return: Ответ с формой обновления информации о пользователе или перенаправление на список пользователей при успешном обновлении.
    """
    model = CustomUser
    fields = ['username', 'role']
    template_name = 'user_update.html' 
    success_url = reverse_lazy('user_list')
    
class UserCreateView(CreateView):
    """
    Создание нового пользователя.

    :param CreateView: Объект представления создания Django.
    :return: Ответ с формой создания нового пользователя или перенаправление на список пользователей при успешном создании.
    """
    model = CustomUser
    fields = ['first_name', 'last_name', 'username', 'role']
    template_name = 'user_create.html'
    success_url = reverse_lazy('user_list')
    
def user_delete(request, pk):
    """
    Удаление пользователя.

    :param request: Объект запроса Django.
    :param pk: Primary key пользователя для удаления.
    :return: Перенаправление на список пользователей.
    """
    user = get_object_or_404(CustomUser, id=pk)
    user.delete()
    return redirect('user_list')
  
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Обновление профиля пользователя.

    :param LoginRequiredMixin: Миксин для проверки авторизации пользователя.
    :param UpdateView: Объект представления обновления Django.
    :return: Ответ с формой обновления профиля пользователя.
    """
    model = CustomUser
    fields = ['username']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
      
class TakeBookView(View):
    def post(self, request, book_id):
        if request.user.is_authenticated:
            book = Book.objects.get(pk=book_id)
            loan_history = LoanHistory(user=request.user, book=book, loan_date=timezone.now())
            loan_history.save()
        return redirect('profile')