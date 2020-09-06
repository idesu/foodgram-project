import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, Ingredient, Tag


@transaction.atomic
def validate_ingredients_and_add_to_recipe(request, recipe_instance) -> None:
    """Вспомогательная функция для проверки и сохранения ингредиентов."""

    recipeingredients = []
    for key, val in request.POST.items():
        if key.startswith('nameIngredient'):
            ingredient_number = key.strip('nameIngredient_')
            #  Может и не быть в случае с "по вкусу"
            ingredient_amount = request.POST.get(f'valueIngredient_{ingredient_number}', None)
            ingredient_amount = int(ingredient_amount) if ingredient_amount else None
            ingredient = get_object_or_404(Ingredient, title=val)
            recipeingredients.append(
                {'recipe': recipe_instance, 'ingredient': ingredient, 'amount': ingredient_amount}
            )

    for recipeingredient in recipeingredients:
        form = RecipeIngredientForm(data=recipeingredient)
        if form.is_valid():
            form.save()
        else:
            raise ValidationError(f'ingredient {recipeingredient} is invalid')


@login_required
def new_recipe(request):
    if request.method == 'POST':
        recipe_instance = Recipe(author=request.user)
        form = RecipeForm(
            request.POST, files=request.FILES or None, instance=recipe_instance)
        if form.is_valid():
            with transaction.atomic():
                try:
                    form.save()
                    validate_ingredients_and_add_to_recipe(request, recipe_instance)
                    for tag in Tag.objects.all():
                        if request.POST.get(tag.title, None) == 'on':
                            recipe_instance.tags.add(tag)
                    #  TODO: Перенаправлять на index
                    return redirect('password_change')
                except ValidationError as error:
                    form.add_error(field='ingredient', error=error)
        return render(request, 'formRecipe.html', {'form': form, })

    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form, })


def get_ingredients(request):
    search_query = Ingredient.objects.filter(title__istartswith=request.GET.get('query', None))[:5]
    results = [{"title": result.title, "dimension": result.measurement.title} for result in search_query]
    result_json = json.dumps(results)
    print(result_json)
    return HttpResponse(result_json, content_type='application/json')
