from django import forms
from .models import *

class FeedbackForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введи имя'}),
        label='Имя'
        )
    text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введи отзыв'}),
        label='Сообщение'
        )
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Введи телефон'}),
        label='Телефон'
    )


class AddBook(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите название книги'}),
        label='Название книги'
        )
    author = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите автора книги'}),
        label='Автор книги'
        )
    price = forms.IntegerField(min_value=0, max_value=10000, label='Стоимость книги')
    genre = forms.ModelChoiceField(label='Выберите жанр', queryset=Genre.objects.all())
    cover_image = forms.ImageField(label='Картинка')

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.lower() in ['перец']:
            raise forms.ValidationError('Этот товар запрещен')
        return name


class GenreForm(forms.ModelForm):
    clear_image = forms.BooleanField(
        required=False,
        label='Удалить текущее изображение'
    )
    
    class Meta:
        model = Genre
        fields = ['name', 'cover_image']
        labels = {
            'name': 'Название жанра',
            'cover_image': 'Обложка жанра',
        }


class AddNews(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите название новости'}),
        label='Название новости'
        )
    desc = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите описание новости'}),
        label='Описание новости'
        )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите текст новости',
            'rows': 10
        }),
        label='Текст новости'
    )
    created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Дата создания',
        required=False
    )
    cover_image = forms.ImageField(label='Картинка')

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.lower() in ['перец']:
            raise forms.ValidationError('Этот товар запрещен')
        return name


class EditNews(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите название новости'}),
        label='Название новости'
    )
    desc = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите описание новости'}),
        label='Описание новости'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите текст новости',
            'rows': 10
        }),
        label='Текст новости'
    )
    created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Дата создания',
        required=False
    )
    cover_image = forms.ImageField(
        label='Картинка',
        required=False
    )
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        initial = kwargs.get('initial', {})
        if self.instance:
            if self.instance.created_at:
                created_at_formatted = self.instance.created_at.strftime('%Y-%m-%dT%H:%M')
            else:
                created_at_formatted = None
            initial.update({
                'name': self.instance.name,
                'desc': self.instance.desc,
                'text': self.instance.text,
                'created_at': created_at_formatted,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.cover_image:
            self.fields['cover_image'].help_text = f'Текущее изображение: {self.instance.cover_image.name}'

    def save(self):
        if not self.instance:
            raise ValueError("Instance is required for EditNewsForm")
        self.instance.name = self.cleaned_data['name']
        self.instance.desc = self.cleaned_data['desc']
        self.instance.text = self.cleaned_data['text']
        self.instance.created_at = self.cleaned_data['created_at']
        if self.cleaned_data['cover_image']:
            self.instance.cover_image = self.cleaned_data['cover_image']
        self.instance.save()
        
        return self.instance
    
class EditBook(forms.Form):
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите название книги'}),
        label='Название книги'
        )
    author = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите автора книги'}),
        label='Автор книги'
        )
    price = forms.IntegerField(min_value=0, max_value=10000, label='Стоимость книги')
    genre = forms.ModelChoiceField(label='Выберите жанр', queryset=Genre.objects.all())
    
    cover_image = forms.ImageField(
        label='Картинка',
        required=False
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.lower() in ['перец']:
            raise forms.ValidationError('Этот товар запрещен')
        return name
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        initial = kwargs.get('initial', {})
        if self.instance:
            initial.update({
                'title': self.instance.title,
                'author': self.instance.author,
                'price': self.instance.price,
                'genre': self.instance.genre,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.cover_image:
            self.fields['cover_image'].help_text = f'Текущее изображение: {self.instance.cover_image.name}'

    def save(self):
        if not self.instance:
            raise ValueError("Instance is required for EditBookForm")
        self.instance.name = self.cleaned_data['title']
        self.instance.desc = self.cleaned_data['author']
        self.instance.price = self.cleaned_data['price']
        self.instance.genre = self.cleaned_data['genre']
        if self.cleaned_data['cover_image']:
            self.instance.cover_image = self.cleaned_data['cover_image']
        self.instance.save()
        
        return self.instance

    