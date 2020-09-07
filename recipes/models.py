from django.contrib.auth import get_user_model
from django.db import models

from recipes.mixins import AutoDateMixin

User = get_user_model()
GRAM_ID = 1


class Tag(models.Model):
    slug = models.SlugField('Название', max_length=35, unique=True)

    def __str__(self):
        return self.slug


class Measurement(models.Model):
    title = models.CharField('Название меры весов', max_length=30, unique=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=100)
    measurement = models.ForeignKey(
        Measurement,
        default=GRAM_ID,
        on_delete=models.SET_DEFAULT,
        related_name='ingredients'
    )

    def __str__(self):
        return self.title


class Recipe(AutoDateMixin, models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    image = models.ImageField('Изображение блюда', upload_to='recipes/')
    description = models.TextField('Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        blank=True,
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.IntegerField('Время приготовления')

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Количество ингредиентов в рецепте."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipeingredients')
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.title}'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.user} - {self.author}'


class BookmarkRecipe(AutoDateMixin, models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='bookmarked')

    def __str__(self):
        return f'{self.user} - {self.recipe.title}'
