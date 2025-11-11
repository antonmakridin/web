from django import forms
from .models import Genre

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