from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Tag, Article, Comment, Rating, Like, Dislike,
    CookingTool, Ingredient, Recipe, RecipeStep, RecipeIngredient, CartItem
)
"""
이 모듈은 Django REST Framework를 활용하여 직렬화(serialization)를 처리하는 여러 Serializer를 정의합니다.  
사용자(User), 게시글(Article), 댓글(Comment), 평가(Rating), 좋아요/싫어요(Like/Dislike),  
요리 도구(Cooking Tool), 재료(Ingredient), 레시피(Recipe), 장바구니 항목(Cart Item) 등과 같은  
모델 데이터를 JSON 형식으로 변환하거나, 클라이언트에서 전달받은 데이터를 처리하기 위한 역할을 합니다.

Classes:
- UserSerializer: Django User 모델 데이터를 직렬화합니다.
- CategorySerializer: 카테고리(Category) 모델 데이터를 직렬화합니다.
- TagSerializer: 태그(Tag) 모델 데이터를 직렬화합니다.
- CommentSerializer: 댓글(Comment) 모델 데이터를 직렬화하며, 작성자(author) 정보를 포함합니다.
- RatingSerializer: 평가(Rating) 모델 데이터를 직렬화하며, 사용자(user) 정보를 포함합니다.
- LikeSerializer: 좋아요(Like) 모델 데이터를 직렬화하며, 사용자(user) 정보를 포함합니다.
- DislikeSerializer: 싫어요(Dislike) 모델 데이터를 직렬화하며, 사용자(user) 정보를 포함합니다.
- ArticleSerializer: 게시글(Article) 모델 데이터를 직렬화하며, 댓글, 평가, 좋아요, 싫어요 등 관련 데이터를 포함합니다.
- CookingToolSerializer: 요리 도구(Cooking Tool) 모델 데이터를 직렬화합니다.
- IngredientSerializer: 재료(Ingredient) 모델 데이터를 직렬화합니다.
- RecipeStepSerializer: 레시피 단계(Recipe Step) 데이터를 직렬화합니다.
- RecipeIngredientSerializer: 레시피 재료(Recipe Ingredient) 데이터를 직렬화하며, 재료 세부 정보를 포함합니다.
- RecipeSerializer: 레시피(Recipe) 모델 데이터를 직렬화하며, 작성자(author), 단계(steps), 재료(ingredients), 도구(tools) 등 관련 데이터를 포함합니다.
- CartItemSerializer: 장바구니 항목(Cart Item) 데이터를 직렬화하며, 총 가격(total_price) 계산 및 재고 검증 기능을 포함합니다.

Methods:
- get_average_rating: ArticleSerializer에서 각 게시글의 평균 평가 점수를 계산합니다.
- validate_quantity: CartItemSerializer에서 수량(quantity)이 1 이상인지 검증합니다.
- validate: CartItemSerializer에서 재고(stock) 검증을 수행합니다.
"""

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