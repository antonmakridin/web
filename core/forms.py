from django import forms

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