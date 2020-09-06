from django.forms import ModelForm

from .models import Recipe, RecipeIngredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image', 'cooking_time',)


class RecipeIngredientForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'amount',)
