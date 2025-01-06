"""
URL configuration for Recommand project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from articles import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("index/", views.index),
    path("article/<int:article_id>/", views.article),
    path("search/", views.search),
    path("author/<str:author_name>/", views.author),
    path("category/<str:category_name>/", views.category),
    path("tag/<str:tag_name>/", views.tag),
    path("feed/", views.feed),
    path("comments/", views.comments),
    path("likes/", views.likes),
    path("dislikes/", views.dislikes),
    path("rate/", views.rate),
    path("upload/", views.upload),
    path("delete/<int:article_id>/", views.delete),
    path("update/<int:article_id>/", views.update),
    path("recommend/", views.recommend),
    path("related/", views.related),
    path("top/", views.top),
    path("search_articles/", views.search_articles),
    path("search_comments/", views.search_comments),
    path("search_likes/", views.search_likes),
    path("search_dislikes/", views.search_dislikes),    
    path("search_rates/", views.search_rates),
    path("search_uploads/", views.search_uploads),
    path("search_deletes/", views.search_deletes),
    path("search_updates/", views.search_updates),
    path("search_recommendations/", views.search_recommendations),
    path("search_related/", views.search_related),
    path("search_tops/", views.search_tops),
]

