from django.shortcuts import render
from django.http import HttpResponse
import math
from .models import *

title = 'Читай САМ'


# Create your views here.
def main(request):
    context = {'title_template': title}
    # получить товары из базы
    genres_list_db = Genre.objects.all()
    context.update( {'genres_list': genres_list_db} )
    return render(request, 'main.html', context)

def catalog(request):
    context = {'image1': 'https://srisovki.ru/wp-content/uploads/2025/05/ryzhij-milyj-kotik-768x959.webp', 'book1' : 'Все о котиках. Часть 1', 'image2': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Zunge_raus.JPG/1200px-Zunge_raus.JPG', 'book2' : 'Все о котиках. Часть 1', 'image3': 'https://srisovki.ru/wp-content/uploads/2024/10/kotik-akula-768x987.webp', 'book3' : 'Все о котиках. Часть 1'}
    return render(request, 'catalog.html', context)

def products(request):
    # получить товары из базы
    products_list_db = Product.objects.all()
    context = {'products_list': products_list_db}
    return render(request, 'products.html', context)

def book_in_genre(request):
    # получить все книги
    books_list_db = Book.objects.all()
    context = {'books_list': books_list_db}
    return render(request, 'book_in_genre.html', context)


def branch(request):
    branch_list = [
        {'name': 'Северный', 'address': 'г. Нижний Тагил, ул. Ленина, д. 5'},
        {'name': 'Южный', 'address': 'г. Сысерть, ул. Малышева, д. 17'},
        {'name': 'Западный', 'address': 'г. Краснофимск, ул. Мизерова, д. 17'}
    ]
    context = {'branch_list': branch_list}
    return render(request, 'branch.html', context)