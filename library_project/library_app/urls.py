from django.urls import path, include
from library_app.views import login_view, register_view
from django.contrib.auth.decorators import login_required
from .views import BookListView, logout_view, BookUpdateView, BookDetailView, delete_book, BookCreateView, HistoryListView, HistoryUpdateView, history_delete, HistoryCreateView, AuthorListView, AuthorCreateView, AuthorUpdateView, author_delete, UserCreateView, UserUpdateView, UsersListView, user_delete, ProfileUpdateView, AuthorDetailView, TakeBookView

urlpatterns = [
    path('', login_view, name='auth'),
    path('register/', register_view, name='register'),
    path('books/', BookListView.as_view(), name='books'),
    path('logout/', logout_view, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/delete/', delete_book, name='book_delete'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('history/', HistoryListView.as_view(), name='history_list'),
    path('history/<int:pk>/edit/', HistoryUpdateView.as_view(), name='history_edit'),
    path('history/<int:pk>/delete/', history_delete, name='history_delete'),
    path('history/create/', HistoryCreateView.as_view(), name='history_create'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/create/', AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<int:pk>/delete/', author_delete, name='author_delete'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('users/', UsersListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', user_delete, name='user_delete'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('profile/', login_required(ProfileUpdateView.as_view()), name='profile'),
    path('take_book/<int:book_id>/', TakeBookView.as_view(), name='take_book'),
]
