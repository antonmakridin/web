from django.shortcuts import render
from django.http import HttpResponse
import math

# Create your views here.
def main(request):
    title = 'Читай САМ'
    context = {'title_template': title}
    return render(request, 'mytpl.html', context)

def catalog(request):
    context = {'image1': 'https://srisovki.ru/wp-content/uploads/2025/05/ryzhij-milyj-kotik-768x959.webp', 'book1' : 'Все о котиках. Часть 1', 'image2': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Zunge_raus.JPG/1200px-Zunge_raus.JPG', 'book2' : 'Все о котиках. Часть 1', 'image3': 'https://srisovki.ru/wp-content/uploads/2024/10/kotik-akula-768x987.webp', 'book3' : 'Все о котиках. Часть 1'}
    return render(request, 'catalog.html', context)