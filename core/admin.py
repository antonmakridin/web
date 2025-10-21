from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Product)
admin.site.register(Genre)
admin.site.register(Branchs)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'price']
    list_filter = ['genre', 'author']