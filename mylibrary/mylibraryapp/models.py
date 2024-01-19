from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Модель для представлення книги
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    release_year = models.IntegerField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Клас-менеджер для користувачів, що розширює BaseUserManager
class CustomUserManager(BaseUserManager):
    # Метод для створення звичайного користувача
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Метод для створення суперкористувача
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# Клас користувача, що розширює AbstractBaseUser
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager() # Призначаємо об'єкт менеджера користувача

    USERNAME_FIELD = 'username' # Поле, що використовується для унікальної ідентифікації користувача
    REQUIRED_FIELDS = [] # Поля, які обов'язково повинні бути вказані при створенні користувача
 
    def __str__(self):
        return self.username