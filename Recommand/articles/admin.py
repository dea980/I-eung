from django.contrib import admin
from .models import (
    Category, Tag, Article, Comment, Rating, Like, Dislike,
    CookingTool, Ingredient, Recipe, RecipeStep, RecipeIngredient, CartItem
)

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

# New admin registrations for cooking and shopping features

@admin.register(CookingTool)
class CookingToolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'unit', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('unit',)
    ordering = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time', 'difficulty', 'serving_size')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('name', 'description', 'author__username')
    filter_horizontal = ('tools',)
    ordering = ('-created_at',)

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'step_number', 'description')
    list_filter = ('recipe',)
    search_fields = ('recipe__name', 'description')
    ordering = ('recipe', 'step_number')

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity', 'unit')
    list_filter = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')
    ordering = ('recipe', 'ingredient')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'ingredient__name')
    ordering = ('-created_at',)
