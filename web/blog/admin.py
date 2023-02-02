from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'author', 'created', 'updated', 'image')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'created', 'updated') # Задает последовательность полей внутри каждой статьи
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')  # поля ForeignKey - чтобы попасть в связанную таблицу
    list_filter = ('status',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'user', 'article', 'created', 'updated', 'parent')
    list_filter = ('article',)
    ordering = ('-updated',)
