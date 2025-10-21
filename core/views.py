from django.shortcuts import render
from django.http import HttpResponse
import math
from .models import *

title = 'Читай САМ'
context = {'title_template': title}


# Create your views here.
def main(request):
    # получить товары из базы
    genres_list_db = Genre.objects.all()
    context.update( {'genres_list': genres_list_db} )
    return render(request, 'main.html', context)

def genres(request, genres_id):
    books_list_db = Book.objects.filter(genre_id=genres_id)
    context = {'books_list': books_list_db}
    return render(request, 'genres.html', context)

def products(request):
    # получить товары из базы
    products_list_db = Product.objects.all()
    context = {'products_list': products_list_db}
    return render(request, 'products.html', context)

def book(request, book_id):
    books_list_db = Book.objects.filter(id=book_id)
    context = {'books_list': books_list_db}
    return render(request, 'book.html', context)


def branch(request):
    # получить все книги
    branch_list_db = Branchs.objects.all().order_by('name')
    context.update({'branch_list': branch_list_db})
    return render(request, 'branch.html', context)