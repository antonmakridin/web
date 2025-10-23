from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import *

def get_base_context():
    return {
        'title_template': 'Читай САМ',
        'root_pages': Page.objects.filter(parent__isnull=True, is_active=True).order_by('order')
    }

# Create your views here.
def main(request):
    genres_list_db = Genre.objects.all()
    
    context = get_base_context()
    context.update({
        'genres_list': genres_list_db,
    })
    return render(request, 'main.html', context)

def genres(request, genre_url, genres_id):
    genre = get_object_or_404(Genre, id=genres_id)
    books_list_db = Book.objects.filter(genre_id=genres_id)
    
    context = get_base_context()
    context.update({
        'books_list': books_list_db,
        'genre': genre,
    })
    return render(request, 'genres.html', context)

def products(request):
    products_list_db = Product.objects.all()
    
    context = get_base_context()
    context.update({
        'products_list': products_list_db,
    })
    return render(request, 'products.html', context)


def book(request, genre_url, genres_id, book_url, book_id):
    book_obj = get_object_or_404(Book, id=book_id, genre_id=genres_id)
    
    context = get_base_context()
    context.update({
        'book': book_obj,
        'genre': book_obj.genre,
    })
    return render(request, 'book.html', context)


def branch(request):
    branch_list_db = Branchs.objects.all().order_by('name')
    
    context = get_base_context()
    context.update({
        'branch_list': branch_list_db,
    })
    return render(request, 'branch.html', context)

def dynamic_page(request, url):
    # обрабатываем динамические страницы
    try:
        # редирект на главную, если урл пустой
        if not url or url == '/':
            return main(request)
            
        # убираем слэши
        clean_url = url.strip('/')
        
        # если URL пустой после очистки - редиректим на главную страницу
        if not clean_url:
            return main(request)
            
        # разбирем урл на части
        url_parts = clean_url.split('/')
        
        # ищем страницу по полному пути
        current_page = None
        
        for part in url_parts:
            if current_page:
                # ищем дочернюю страницу
                current_page = get_object_or_404(
                    Page, 
                    url=part, 
                    parent=current_page, 
                    is_active=True
                )
            else:
                # ищем родительскую страницу
                current_page = get_object_or_404(
                    Page, 
                    url=part, 
                    parent__isnull=True, 
                    is_active=True
                )
        
        # получаем дочерние страницы
        children_pages = current_page.children.filter(is_active=True).order_by('order')
        
        context = get_base_context()
        context.update({
            'page': current_page,
            'children_pages': children_pages,
            'breadcrumbs': current_page.get_breadcrumbs(),
        })
        
        return render(request, 'page.html', context)
        
    except Http404:
        print(f"Page not found: {url}")
        raise Http404("Страница не найдена")
    except Exception as e:
        print(f"Error loading page {url}: {str(e)}")
        raise Http404("Ошибка при загрузке страницы")