from django.urls import path
from .views import * 
"""импортируем все функции из views"""

urlpatterns = [
    path('', main),
    path('hello/', hello),
    path('pi/', pi),
    path('name/', name),
]