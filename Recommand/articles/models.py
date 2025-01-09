from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """
    Represents a category for grouping articles.

    Attributes:
        name (str): The unique name of the category.
        description (str): A brief description of the category.
        created_at (datetime): The timestamp when the category was created.
        updated_at (datetime): The timestamp when the category was last updated.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    Represents a tag for categorizing articles.

    Attributes:
        name (str): The unique name of the tag.
        created_at (datetime): The timestamp when the tag was created.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    """
    Represents a blog article.

    Attributes:
        title (str): The title of the article.
        content (str): The content of the article.
        author (User): The author of the article.
        category (Category): The category of the article.
        tags (ManyToManyField): The tags associated with the article.
        created_at (datetime): The timestamp when the article was created.
        updated_at (datetime): The timestamp when the article was last updated.
        views_count (int): The number of times the article has been viewed.
        likes_count (int): The number of times the article has been liked.
        dislikes_count (int): The number of times the article has been disliked.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Represents a comment on an article.

    Attributes:
        article (Article): The article the comment is associated with.
        author (User): The user who wrote the comment.
        content (str): The content of the comment.
        created_at (datetime): The timestamp when the comment was created.
        updated_at (datetime): The timestamp when the comment was last updated.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'

class Rating(models.Model):
    """

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    Represents a user rating for an article.

    Attributes:
        article (Article): The article being rated.
        user (User): The user who provided the rating.
        value (int): The rating value (1-5).
        created_at (datetime): The timestamp when the rating was created.

    Meta:
        unique_together: Ensures a user can rate an article only once.
    
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['article', 'user']

    def __str__(self):
        return f'{self.user.username} rated {self.article.title}: {self.value} stars'

class Like(models.Model):
    """
    Represents a like for an article by a user.

    Attributes:
        article (Article): The article being liked.
        user (User): The user who liked the article.
        created_at (datetime): The timestamp when the like was created.

    Meta:
        unique_together: Ensures a user can like an article only once.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['article', 'user']

    def __str__(self):
        return f'{self.user.username} liked {self.article.title}'

class Dislike(models.Model):
    """
    Represents a dislike for an article by a user.

    Attributes:
        article (Article): The article being disliked.
        user (User): The user who disliked the article.
        created_at (datetime): The timestamp when the dislike was created.

    Meta:
        unique_together: Ensures a user can dislike an article only once.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['article', 'user']

    def __str__(self):
        return f'{self.user.username} disliked {self.article.title}'

# New models for cooking and shopping features

class CookingTool(models.Model):
    """
    Represents a cooking tool used in recipes.

    Attributes:
        name (str): The name of the cooking tool.
        description (str): A description of the tool.
        image (ImageField): An optional image of the tool.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='cooking_tools/', null=True, blank=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """
    Represents an ingredient for cooking or recipes.

    Attributes:
        name (str): The name of the ingredient.
        description (str): A description of the ingredient.
        price (decimal): The price of the ingredient.
        unit (str): The unit of measurement (e.g., "kg", "개").
        stock (int): The available stock of the ingredient.
        image (ImageField): An optional image of the ingredient.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)  # e.g., "kg", "개", "ml"
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='ingredients/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Recipe(models.Model):
    """
    Represents a cooking recipe.

    Attributes:
        name (str): The name of the recipe.
        author (User): The user who created the recipe.
        description (str): A description of the recipe.
        cooking_time (int): Cooking time in minutes.
        difficulty (str): The difficulty level of the recipe.
        serving_size (int): The number of servings.
        tools (CookingTool): The tools required for the recipe.
        created_at (datetime): The timestamp when the recipe was created.
        updated_at (datetime): The timestamp when the recipe was last updated.
        image (ImageField): An optional image of the completed recipe.
    """
    DIFFICULTY_CHOICES = [
        ('easy', '쉬움'),
        ('medium', '보통'),
        ('hard', '어려움'),
    ]

    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    description = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="조리 시간(분)")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    serving_size = models.PositiveIntegerField(help_text="몇 인분")
    tools = models.ManyToManyField(CookingTool, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeStep(models.Model):
    """
    Represents an individual step in a recipe.

    Attributes:
        recipe (Recipe): The recipe this step belongs to.
        step_number (int): The step number.
        description (str): The description of the step.
        image (ImageField): An optional image illustrating the step.

    Meta:
        ordering: Steps are ordered by their step number.
        unique_together: Ensures step numbers are unique within a recipe.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_steps/', null=True, blank=True)

    class Meta:
        ordering = ['step_number']
        unique_together = ['recipe', 'step_number']

    def __str__(self):
        return f"{self.recipe.name} - Step {self.step_number}"

class RecipeIngredient(models.Model):
    """
    Represents an ingredient used in a recipe.

    Attributes:
        recipe (Recipe): The recipe this ingredient belongs to.
        ingredient (Ingredient): The ingredient used.
        quantity (decimal): The quantity of the ingredient.
        unit (str): The unit of the ingredient for the recipe.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipes')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)  # 레시피별 단위 (예: "큰술", "작은술" 등)

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"

class CartItem(models.Model):
    """
    Represents a shopping cart item for purchasing ingredients.

    Attributes:
        user (User): The user who owns the cart.
        ingredient (Ingredient): The ingredient in the cart.
        quantity (int): The quantity of the ingredient.
        created_at (datetime): The timestamp when the item was added to the cart.
        updated_at (datetime): The timestamp when the item was last updated.

    Methods:
        total_price: Calculates the total price for the cart item.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'ingredient']

    @property
    def total_price(self):
        return self.ingredient.price * self.quantity

    def __str__(self):
        return f"{self.user.username}'s cart - {self.ingredient.name}"
