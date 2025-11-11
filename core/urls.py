from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import * 
"""импортируем все функции из views"""

urlpatterns = [
    path('', main),
    # path('catalog/', catalog),
    path('products/', products),
    path('feedback/', add_feedback),
    path('branch/', branch),
    path('book/add', add_product),
    path('genre/add', add_genre),
    path('branch/add', add_branch),
    path('genres/<slug:genre_url>-<int:genres_id>/', genres, name='genre_detail'),
    path('genres/<slug:genre_url>-<int:genres_id>/book/<slug:book_url>-<int:book_id>/', book, name='book_detail'),
# динамические урлы
    re_path(r'^(?P<url>.*)/$', dynamic_page, name='dynamic_page'),
]
handler404 = 'web.views.custom_404_view'