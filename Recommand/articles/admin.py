from django.contrib import admin
from .models import Category, Tag, Article, Comment, Rating, Like, Dislike

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'views_count', 'likes_count')
    list_filter = ('category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count', 'likes_count', 'dislikes_count')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'article__title')
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)
