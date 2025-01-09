from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Tag, Article, Comment, Rating, Like, Dislike,
    CookingTool, Ingredient, Recipe, RecipeStep, RecipeIngredient, CartItem
)

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

# New serializers for cooking and shopping features

class CookingToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingTool
        fields = ['id', 'name', 'description', 'image']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'price', 'unit', 'stock', 'image']

class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['id', 'recipe', 'step_number', 'description', 'image']
        read_only_fields = ['recipe']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_details = IngredientSerializer(source='ingredient', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'ingredient', 'ingredient_details', 'quantity', 'unit']
        read_only_fields = ['recipe']

class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    tools = CookingToolSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'author', 'description', 'cooking_time',
            'difficulty', 'serving_size', 'tools', 'ingredients',
            'steps', 'created_at', 'updated_at', 'image'
        ]
        read_only_fields = ['author']

    def create(self, validated_data):
        tools_data = self.context['request'].data.get('tools', [])
        ingredients_data = self.context['request'].data.get('ingredients', [])
        steps_data = self.context['request'].data.get('steps', [])

        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

        # Add tools
        recipe.tools.set(tools_data)

        # Add ingredients
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data['ingredient'],
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )

        # Add steps
        for step_data in steps_data:
            RecipeStep.objects.create(
                recipe=recipe,
                step_number=step_data['step_number'],
                description=step_data['description'],
                image=step_data.get('image')
            )

        return recipe

class CartItemSerializer(serializers.ModelSerializer):
    ingredient_details = IngredientSerializer(source='ingredient', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'ingredient', 'ingredient_details', 'quantity', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_price']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("수량은 1개 이상이어야 합니다.")
        return value

    def validate(self, data):
        ingredient = data['ingredient']
        quantity = data['quantity']
        
        if quantity > ingredient.stock:
            raise serializers.ValidationError(f"재고가 부족합니다. 현재 재고: {ingredient.stock}")
        return data