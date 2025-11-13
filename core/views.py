from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *


def get_base_context():
    return {
        'title_template': 'Читай САМ',
        'root_pages': Page.objects.filter(parent__isnull=True, is_active=True).order_by('order'),
        'genres_list': Genre.objects.all()
    }

# Create your views here.
def main(request):
    news_list_db = News.objects.all().order_by('-created_at')[:3]
    
    context = get_base_context()
    context.update({
        'news_list': news_list_db,
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
    

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def page_not_found(request, exception):
    return render(request, '404.html', status=404) 

def add_product_old(request):
    error = ''
    print(request.POST)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        genre = request.POST.get('genre')        
        image = request.FILES.get('image')

        if title and author and price and genre:
            Book.objects.create(
                title=title,
                author=author,
                price=price,
                genre_id=genre,
                cover_image=image
            )
            return redirect('/')
        else:
            error = 'Заполните все поля'
    genres_list_db = Genre.objects.all()
    context = get_base_context()
    context.update({
        'genres_list': genres_list_db,
        'error': error,
    })
    return render(request, 'add_product.html', context)

# добавление жанра
def add_genre(request):
    error = ''
    print(request.POST)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        # Создаем экземпляр модели и сохраняем данные
        if name:
            genre = Genre.objects.create(
                name=name,
                cover_image=image
            )
            return redirect(genre.get_absolute_url())
        else:
            error = 'Заполните все поля'
    genres_list_db = Genre.objects.all()
    context = get_base_context()
    context.update({
        'genres_list': genres_list_db,
        'error': error,
    })
    return render(request, 'add_genre.html', context)


# удаление жанра
def delete_genre(request, genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
        genre.delete()
        # редирект на страниу после удаления
        return redirect('/genre/add')  # или на другую страницу
    except Genre.DoesNotExist:
        # редирект если жанр не найден
        return redirect('/genre/add')

# редактирование жанра
def edit_genre(request,genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
        
        if request.method == 'POST':
            form = GenreForm(request.POST, request.FILES, instance=genre)
            if form.is_valid():
                genre = form.save(commit=False)
                if form.cleaned_data['clear_image']:
                    genre.cover_image.delete(save=False)
                    genre.cover_image = None
                genre.save()
                return redirect('/genre/add')
        else:
            form = GenreForm(instance=genre)
        
        context = get_base_context()
        context.update({
            'form': form,
            'genre': genre,
        })
        return render(request, 'edit_genre.html', context)
        
    except Genre.DoesNotExist:
        return redirect('/')
        
    except Genre.DoesNotExist:
        return redirect('/')


# добавление филиала
def add_branch(request):
    error = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        text = request.POST.get('text')
        rate = request.POST.get('rate')
        
        # Создаем экземпляр модели и сохраняем данные
        if name and address and text and rate:
            Branchs.objects.create(
                name=name,
                address=address,
                text=text,
                rate=rate
            )
            return redirect('/')
        else:
            error = 'Заполните все поля'

    branch_list_db = Branchs.objects.all()
    
    context = get_base_context()
    context.update({
        'branch_list': branch_list_db,
        'error': error,
    })


    return render(request, 'add_branch.html', context)


def add_feedback_old(request):
    error = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        phone = request.POST.get('phone')
        
        
        # Создаем экземпляр модели и сохраняем данные
        if name and text and phone:
            Feedback.objects.create(
                name=name,
                text=text,
                phone = phone
            )
            return redirect('/')
        else:
            error = 'Заполните все поля'
    genres_list_db = Genre.objects.all()
    context = get_base_context()
    context.update({
        'genres_list': genres_list_db,
        'error': error,
    })
    return render(request, 'add_feedback.html', context)


def add_feedback(request):
    feedback_form = FeedbackForm(request.POST)
    if feedback_form.is_valid():
        name = request.POST.get('name')
        text = request.POST.get('text')
        phone = request.POST.get('phone')
        Feedback.objects.create(
            name=name,
            text=text,
            phone = phone
        )
        return redirect('/feedback/')
    
    context = {'feedback_form': feedback_form}
    return render(request, 'add_feedback.html', context)


def add_product(request):
    form = AddBook()
    if request.method == 'POST':
        form = AddBook(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            book = Book.objects.create(**data)
            
            return redirect(book.get_absolute_url())

    context = get_base_context()
    context.update = {
        'form': form
    }
    return render(request, 'add_product.html', context)



# НОВОСТИ
def add_news(request):
    form = AddNews()
    if request.method == 'POST':
        form = AddNews(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            news = News.objects.create(**data)
            
            return redirect(news.get_absolute_url())

    context = get_base_context()
    context = {
        'page_title': f'Добавление новости',
        'form': form
    }
    return render(request, 'news_add.html', context)


def edit_news(request, news_url):
    news_obj = get_object_or_404(News, url=news_url)
    
    if request.method == 'POST':
        form = EditNews(request.POST, request.FILES, instance=news_obj)
        if form.is_valid():
            news = form.save()
            return redirect(news.get_absolute_url())
    else:
        form = EditNews(instance=news_obj)
    
    context = get_base_context()
    context.update({
        'form': form,
        'news': news_obj,
        'page_title': f'Редактирование новости: {news_obj.name}',
        'submit_text': 'Сохранить изменения',
        'is_edit': True
    })
    return render(request, 'news_edit.html', context)


def delete_news(request, news_url):
    news_obj = get_object_or_404(News, url=news_url)
    
    if request.method == 'POST':
        news_obj.delete()
        return redirect('list_news')
    
    context = get_base_context()
    context.update({
        'news': news_obj
    })
    return render(request, 'news_delete.html', context)


def list_news(request):
    news_list_db = News.objects.all().order_by('-created_at')
    
    news_on_page = 5
    paginator = Paginator(news_list_db, news_on_page)
    page = request.GET.get('page')
    
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    context = get_base_context()
    context.update({
        'news_list': news_list,
    })
    return render(request, 'news.html', context)


def show_news(request, news_url):
    news_obj = get_object_or_404(News, url=news_url)
    
    context = get_base_context()
    context.update({
        'news': news_obj,
    })
    return render(request, 'news_show.html', context)

