from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from .utils.file_rename import BookFileRenamer
from .utils.generate_url import URLGenerator

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
    url = models.CharField(
        max_length=255, 
        verbose_name='URL',
        blank=True,
        unique=True,
        help_text='URL (генерируется автоматически)'
    )
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.url:
            # Генерируем базовый slug
            base_slug = URLGenerator.generate_slug(self.name)
            # Делаем его уникальным
            self.url = URLGenerator.make_unique_slug(Genre, base_slug, self)
                
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('genre_detail', kwargs={
            'genre_url': self.url,
            'genres_id': self.id
        })


# таблица новостей
class News(models.Model):
    name = models.CharField(max_length=1500, verbose_name='Название новости')
    desc = models.CharField(max_length=5000, verbose_name='Описание новости')
    text = RichTextField(verbose_name='Содержание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # Изображение жанра
    cover_image = models.ImageField(
        upload_to=BookFileRenamer.rename_cover,
        verbose_name='Обложка новости',
        blank=True,
        null=True
    )
    url = models.CharField(
        max_length=255, 
        verbose_name='URL',
        blank=True,
        unique=True,
        help_text='URL (генерируется автоматически)'
    )
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.url:
            # Генерируем базовый slug
            base_slug = URLGenerator.generate_slug(self.name)
            # Делаем его уникальным
            self.url = URLGenerator.make_unique_slug(News, base_slug, self)
                
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('show_news', kwargs={
            'news_url': self.url
        })

# таблица книг
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, verbose_name='Автор')
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Жанр'
    )
    price = models.IntegerField(verbose_name='Цена')
    url = models.CharField(
        max_length=255, 
        verbose_name='URL',
        blank=True,
        unique=True,
        help_text='URL (генерируется автоматически)'
    )
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
    
    def save(self, *args, **kwargs):
        print(kwargs)
        print(args)
        if not self.url:
            # генерируем slug
            base_slug = URLGenerator.generate_slug(self.title)
            
            if self.genre:
                # Делаем slug уникальным для жанра
                self.url = URLGenerator.make_unique_slug(
                    Book, base_slug, self, genre=self.genre
                )
            else:
                # Делаем slug уникальным
                self.url = URLGenerator.make_unique_slug(Book, base_slug, self)
                
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('book_detail', kwargs={
            'genre_url': self.genre.url,
            'genres_id': self.genre.id,
            'book_url': self.url,
            'book_id': self.id
        })

# таблица филиалов
class Branchs(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    text = models.CharField(
        max_length=250, 
        null=True,
        blank=True,
        verbose_name='какой-то текст'
        )
    rate = models.IntegerField(default=1, verbose_name='Рейтинг')

    # чтобы отображались красивые названия в админке
    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name
    
# таблица страниц
class Page(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название страницы')
    url = models.SlugField(
        max_length=255, 
        verbose_name='URL',
        blank=True,
        help_text='URL страницы (генерируется автоматически)'
    )
    content = RichTextField(verbose_name='Содержание', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Родительская страница',
        related_name='children'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    meta_title = models.CharField(max_length=255, verbose_name='Meta title', blank=True)
    meta_description = models.TextField(verbose_name='Meta description', blank=True)
    
    # MPTT fields with defaults
    level = models.PositiveIntegerField(default=0, editable=False)
    lft = models.PositiveIntegerField(default=0, editable=False)
    rght = models.PositiveIntegerField(default=0, editable=False)
    tree_id = models.PositiveIntegerField(default=0, editable=False)
    
    class MPTTMeta:
        order_insertion_by = ['order', 'title']
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        unique_together = ['url', 'parent']
    
    def __str__(self):
        return self.title
    
    def get_full_url(self):
        # полный URL страницы с учетом вложенности
        if self.parent:
            return f"{self.parent.get_full_url()}/{self.url}"
        return self.url
    
    def get_breadcrumbs(self):
        # хлебные крошки для страницы
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.insert(0, {'title': current.title, 'url': current.get_full_url()})
            current = current.parent
        return breadcrumbs
    
    def save(self, *args, **kwargs):
        if not self.url:
            base_slug = URLGenerator.generate_slug(self.title)
            
            if self.parent:
                self.url = URLGenerator.make_unique_slug(
                    Page, base_slug, self, parent=self.parent
                )
            else:
                self.url = URLGenerator.make_unique_slug(Page, base_slug, self)
        
        if not self._check_url_uniqueness():
            base_slug = URLGenerator.generate_slug(self.title)
            if self.parent:
                self.url = URLGenerator.make_unique_slug(
                    Page, base_slug, self, parent=self.parent
                )
            else:
                self.url = URLGenerator.make_unique_slug(Page, base_slug, self)
                
        super().save(*args, **kwargs)
    
    def _check_url_uniqueness(self):
        if not self.url:
            return False
            
        existing = Page.objects.filter(url=self.url, parent=self.parent)
        if self.pk:
            existing = existing.exclude(pk=self.pk)
        return not existing.exists()


class Feedback(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    text = models.CharField(verbose_name='Отзыв')
    phone = models.CharField(verbose_name='Телефон')

    # чтобы отображались красивые названия в админке
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name