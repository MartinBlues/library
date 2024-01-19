from django import forms
from .models import Book, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Форма для створення або оновлення екземпляра книги
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Визначаємо поля з моделі Book, які будуть включені до форми
        fields = ['title', 'author', 'genre', 'release_year', 'is_read']

# Форма для реєстрації користувача, на основі UserCreationForm у Django
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Поля, які будуть відображені у формі реєстрації
        fields = ('username', 'password1', 'password2')

# Форма для автентифікації користувача, на основі AuthenticationForm у Django
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        # Поля, які будуть відображені у формі входу
        fields = ('username', 'password')