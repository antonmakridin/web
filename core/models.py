from django.db import models
from .utils.file_rename import BookFileRenamer

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    count = models.IntegerField(verbose_name='Количество')

    # чтобы отображались красивые названия в админке
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

# таблица жанров
class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название жанра')
    # Изображение жанра
    cover_image = models.ImageField(
        upload_to=BookFileRenamer.rename_cover,
        verbose_name='Обложка книги',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name

# таблица книг
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, verbose_name='Автор')
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Жанр'
    )
    price = models.IntegerField(verbose_name='Цена')

    # Поле для загрузки обложки
    cover_image = models.ImageField(
        upload_to=BookFileRenamer.rename_cover,
        verbose_name='Обложка книги',
        blank=True,
        null=True
    )
    
    # Поле для файла
    file = models.FileField(
        upload_to=BookFileRenamer.rename_file,
        verbose_name='Файл',
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'core'
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
    def __str__(self):
        return self.title