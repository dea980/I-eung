from django.contrib import admin
from .models import Category, Tag, Article, Comment, Rating, Like, Dislike
"""
Admin module for managing the admin interface of the blog application.

This module customizes the Django admin site for the models:
- Category: Represents categories for grouping articles.
- Tag: Represents tags for categorizing articles.
- Article: Represents blog articles.
- Comment: Represents comments on articles.
- Rating: Represents user ratings for articles.
- Like: Represents likes on articles.
- Dislike: Represents dislikes on articles.

Each admin class customizes the admin interface for better usability and efficiency.

이 admin.py 모듈은 블로그 애플리케이션의 관리자 인터페이스를 설정합니다.

이 모듈은 다음 모델들의 관리자 화면 구성을 제공합니다:
- Category: 게시글의 카테고리를 나타냅니다.
- Tag: 게시글에 태그를 추가하여 분류를 지원합니다.
- Article: 블로그 게시글을 나타냅니다.
- Comment: 게시글에 달린 댓글을 나타냅니다.
- Rating: 게시글에 대한 사용자의 평점을 나타냅니다.
- Like: 게시글에 대한 '좋아요'를 나타냅니다.
- Dislike: 게시글에 대한 '싫어요'를 나타냅니다.

각 관리자 클래스는 관리자 화면에서 모델을 더 효율적으로 사용할 수 있도록 설정을 커스터마이징합니다.
"""

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Args:
        admin (_type_): _description_
    
    Customizes the admin interface for the Category model.
    Admin configuration for the Category model.

    Displays:
    - Name
    - Creation and update timestamps

    Allows searching by:
    - Name
    - Description

    Orders the list by:
    - Name
    
    """
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Args:
        admin (_type_): _description_
    
    Customizes the admin interface for the Tag model.
    Admin configuration for the Tag model.
    
    Displays:
    - Name
    - Creation timestamp

    Allows searching by:
    - Name

    Orders the list by:
    - Name
    """
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """

    Args:
        admin (_type_): _description_
        
    Customizes the admin interface for the Article model.
    Admin configuration for the Article model.
    
    Displays:
    - Title
    - Author
    - Category
    - Creation and update timestamps
    - Views count
    - Likes count
    
    Allows filtering by:
    - Category
    - Tags
    - Creation timestamp

    Allows searching by:
    - Title
    - Content
    - Author's username
    - Category name

    Orders the list by:
    - Most recently created articles (descending)

    Additional features:
    - Supports horizontal filtering for tags
    - View count, like count, and dislike count are read-only fields
    
    """
    list_display = ('title', 'author', 'category', 'created_at', 'views_count', 'likes_count')
    list_filter = ('category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count', 'likes_count', 'dislikes_count')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """

    Args:
        admin (_type_): _description_
    
    Customizes the admin interface for the Comment model.
    Admin configuration for the Comment model.

    Displays:
    - Article
    - Author
    - Creation timestamp

    Allows filtering by:
    - Creation timestamp

    Allows searching by:
    - Content
    - Author's username
    - Article title

    Orders the list by:
    - Most recently created comments (descending)

    """
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'article__title')
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """

    Args:
        admin (_type_): _description_
        
    Customizes the admin interface for the Rating model.
    Admin configuration for the Rating model.
    Displays:
    - Article
    - User
    - Rating value
    - Creation timestamp

    Allows filtering by:
    - Rating value
    - Creation timestamp

    Allows searching by:
    - Article title
    - User's username

    Orders the list by:
    - Most recently created ratings (descending)
    """
    list_display = ('article', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """

    Args:
        admin (_type_): _description_
    
    Customizes the admin interface for the Like model.
    Admin configuration for the Like model.
    Displays:
    - Article
    - User
    - Creation timestamp

    Allows filtering by:
    - Creation timestamp

    Allows searching by:
    - Article title
    - User's username

    Orders the list by:
    - Most recently created likes (descending)
    """
    list_display = ('article', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    """"

    Args:
        admin (_type_): _description_
    
    Customizes the admin interface for the Dislike model.
    Admin configuration for the Dislike model.
    Displays:
    - Article
    - User
    - Creation timestamp
    
    Allows filtering by:
    - Creation timestamp
    
    Allows searching by:
    - Article title
    - User's username

    Orders the list by:
    - Most recently created dislikes (descending)
    """
    list_display = ('article', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username')
    ordering = ('-created_at',)
