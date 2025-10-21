from django.urls import path
from .views import * 
"""импортируем все функции из views"""

urlpatterns = [
    path('', main),
    # path('catalog/', catalog),
    path('products/', products),
    path('branch/', branch),
    path('book/<int:book_id>', book),
    path('genres/<int:genres_id>', genres),
]