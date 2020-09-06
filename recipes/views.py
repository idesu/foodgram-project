import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RecipeForm
from .models import Recipe, Ingredient, Tag, RecipeIngredient


def validate_ingredients_list(request) -> tuple:
    """функция обрабатывает список ингредиентов с фронтенда и валидирует их наличие в базе."""

    invalid_ingredients = []
    valid_ingredients_data = []
    for key, val in request.POST.items():
        if key.startswith('nameIngredient'):
            ingredient_number = key.strip('nameIngredient_')
            #  Может и не быть в случае с "по вкусу"
            ingredient_amount = request.POST.get(f'valueIngredient_{ingredient_number}', None)
            ingredient_amount = int(ingredient_amount) if ingredient_amount else None
            try:
                ingredient = Ingredient.objects.get(title=val)
                valid_ingredients_data.append({'ingredient': ingredient, 'amount': ingredient_amount})
            except Ingredient.DoesNotExist:
                invalid_ingredients.append(val)
    return valid_ingredients_data, invalid_ingredients


def create_recipeingredients(recipe_instance, valid_ingredients) -> None:
    """Функция сохранения провалидированных ингредиентов для рецента."""
    for recipeingredient in valid_ingredients:
        recipeingredient['recipe'] = recipe_instance
        RecipeIngredient.objects.create(
            recipe=recipe_instance,
            ingredient=recipeingredient['ingredient'],
            amount=recipeingredient['amount'],
        )


def update_tags(request, recipe) -> None:
    recipe.tags.clear()
    for tag in Tag.objects.all():
        if request.POST.get(tag.title, None) == 'on':
            recipe.tags.add(tag)


@login_required
def new_recipe(request):
    if request.method == 'POST':
        recipe_instance = Recipe(author=request.user)
        form = RecipeForm(request.POST, files=request.FILES or None, instance=recipe_instance)
        valid_ingredients, invalid_ingredients = validate_ingredients_list(request)
        if form.is_valid() and not invalid_ingredients:
            with transaction.atomic():
                form.save()
                create_recipeingredients(recipe_instance, valid_ingredients)
                update_tags(request, recipe_instance)
                #  TODO: Перенаправлять на index
            return redirect('password_change')
        else:
            valid = []
            for idx, ingredient in enumerate(valid_ingredients):
                valid.append(
                    {
                        'id': idx + 1,
                        'title': ingredient['ingredient'].title,
                        'amount': ingredient['amount'],
                    }
                )
            form.add_error(field='ingredients',
                           error=ValidationError(f'Ингредиентов {invalid_ingredients} не существует.'))
            return render(request, 'formRecipe.html', {'form': form, 'valid_ingredients': valid})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form, })


# @login_required
# def edit_recipe(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#
#     if request.user != recipe.author:
#         # TODO: Перенаправлять на index
#         return redirect('password_change')
#
#     form = RecipeForm(request.POST, files=request.FILES or None, instance=recipe)
#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     form.save()
#                     validate_ingredients_and_add_to_recipe(request, recipe)
#                     update_tags(request, recipe)
#                     #  TODO: Перенаправлять на index
#                     return redirect('password_change')
#             except ValidationError as error:
#                 form.add_error(field='ingredient', error=error)
#         return render(request, 'formChangeRecipe.html', {'form': form, })
#     return render(request, 'formChangeRecipe.html', {'form': form, })


def get_ingredients(request):
    search_query = Ingredient.objects.filter(title__istartswith=request.GET.get('query', None))[:5]
    results = [{"title": result.title, "dimension": result.measurement.title} for result in search_query]
    result_json = json.dumps(results)
    print(result_json)
    return HttpResponse(result_json, content_type='application/json')
