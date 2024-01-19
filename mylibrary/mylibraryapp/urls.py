from django.urls import path
from .views import BookListView, mark_as_read, edit_book, delete_book, search_books, filter_books, create_book, register
from .views import CustomLoginView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('register/', register, name='register'),
    path('books/<int:pk>/mark_as_read/', mark_as_read, name='mark_as_read'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
    path('search/', search_books, name='search_books'),
    path('filter/', filter_books, name='filter_books'),
    path('books/create/', create_book, name='create_book'),
]