from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Article, Comment, Rating, Like, Dislike

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'article', 'user', 'value', 'created_at']
        read_only_fields = ['user']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'article', 'user', 'created_at']
        read_only_fields = ['user']

class DislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Dislike
        fields = ['id', 'article', 'user', 'created_at']
        read_only_fields = ['user']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    dislikes = DislikeSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'category', 'tags',
            'created_at', 'updated_at', 'views_count', 'likes_count',
            'dislikes_count', 'comments', 'ratings', 'likes', 'dislikes',
            'average_rating'
        ]
        read_only_fields = ['author', 'views_count', 'likes_count', 'dislikes_count']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return None
        return sum(r.value for r in ratings) / len(ratings)

    def create(self, validated_data):
        tags_data = self.context['request'].data.get('tags', [])
        category_id = self.context['request'].data.get('category')
        
        article = Article.objects.create(
            author=self.context['request'].user,
            category_id=category_id,
            **validated_data
        )
        
        # Add tags
        if tags_data:
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)
        
        return article