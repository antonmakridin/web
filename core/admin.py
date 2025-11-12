from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'url', 'order', 'is_active', 'get_full_url_display']
    list_display_links = ['indented_title']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'content']
    prepopulated_fields = {'url': ('title',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'url', 'content', 'parent', 'order', 'is_active')
        }),
        ('SEO настройки', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def indented_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title
        )
    indented_title.short_description = 'Название'
    
    def get_full_url_display(self, obj):
        return format_html('<code>/{}</code>', obj.get_full_url())
    get_full_url_display.short_description = 'Полный URL'
    
    mptt_level_indent = 20


admin.site.register(Product)
admin.site.register(Branchs)
admin.site.register(Feedback)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'price', 'url']
    list_filter = ['genre', 'author']
    prepopulated_fields = {'url': ('title',)}