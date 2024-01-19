from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

# Вьюшка, що відображає список всіх книг
class BookListView(ListView):
    model = Book
    template_name = 'mylibraryapp/book_list.html'
    context_object_name = 'books'

# Вьюшка для створення нової книги
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'mylibraryapp/create_book.html', {'form': form})

# Вьюшка для відмітки книги як прочитаної
def mark_as_read(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_read = True
    book.save()
    return redirect('book_list')

# Вьюшка для редагування існуючої книги
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'mylibraryapp/edit_book.html', {'form': form, 'book': book})

# Вьюшка для видалення книги
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

# Вьюшка для пошуку книг за різними параметрами
def search_books(request):
    query = request.GET.get('search', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) |
        Q(genre__icontains=query) | Q(release_year__icontains=query)
    )
    return render(request, 'mylibraryapp/book_list.html', {'books': books})

# Вьюшка для фільтрації книг за прочитаним/непрочитаним статусом
def filter_books(request):
    read_status = request.GET.get('read_status', '')
    if read_status == 'read':
        books = Book.objects.filter(is_read=True)
    elif read_status == 'unread':
        books = Book.objects.filter(is_read=False)
    else:
        books = Book.objects.all()
    return render(request, 'mylibraryapp/book_list.html', {'books': books})

# Вьюшка для реєстрації нового користувача
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматично логінимо користувача після реєстрації
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Власна вьюшка для логіну, яка використовує адаптовану форму логіну
class CustomLoginView(LoginView):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Перенаправлення на сторінку реєстрації при невірних даних логіну
        response = redirect('register')
        return response

# Вьюшка для логіну користувача
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book_list')  # Змінилось на 'book_list'
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})