from django.shortcuts import render
from django.http import HttpResponse
import math

title = 'Читай САМ'
context = {'title_template': title}

# Create your views here.
def main(request):
    
    return render(request, 'mytpl.html', context)

def catalog(request):
    context.update({'image1': 'https://srisovki.ru/wp-content/uploads/2025/05/ryzhij-milyj-kotik-768x959.webp', 'book1' : 'Все о котиках. Часть 1', 'image2': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Zunge_raus.JPG/1200px-Zunge_raus.JPG', 'book2' : 'Все о котиках. Часть 1', 'image3': 'https://srisovki.ru/wp-content/uploads/2024/10/kotik-akula-768x987.webp', 'book3' : 'Все о котиках. Часть 1'})
    return render(request, 'catalog.html', context)

def products(request):
    products_list = [
        {'name': 'Молоко', 'price': 50, 'discount': True, 'image': 'https://s0.rbk.ru/v6_top_pics/media/img/0/78/756801770042780.webp'},
        {'name': 'Хлеб', 'price': 70, 'discount': False, 'image': 'https://ist.say7.info/img0009/93/993_013292e_5426_1024.jpg'},
        {'name': 'Конфеты', 'price': 20, 'discount': True, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFHDGJtjTJg7D-i8F4G0QlYEy-_w9mlbaMvQ&s'}
    ]

    products = {'products_list': products_list}
    context.update(products)
    return render(request, 'products.html', context)


def branch(request):
    branch_list = [
        {'name': 'Северный', 'address': 'г. Нижний Тагил, ул. Ленина, д. 5'},
        {'name': 'Южный', 'address': 'г. Сысерть, ул. Малышева, д. 17'},
        {'name': 'Западный', 'address': 'г. Краснофимск, ул. Мизерова, д. 17'}
    ]

    branch = {'branch_list': branch_list}
    context.update(branch)
    return render(request, 'branch.html', context)