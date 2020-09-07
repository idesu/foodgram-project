from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image', 'cooking_time', 'ingredients')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
        }
