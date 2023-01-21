from django.contrib import admin
from .models import Category, Post, Author, Comment,Subscribers


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title_news', 'date_time_create')
    list_filter = ('date_time_create',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title_news', 'date_time_create')


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Subscribers)
