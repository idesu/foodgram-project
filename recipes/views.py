import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeForm
from .models import Recipe, Ingredient
from .utils import (
    validate_ingredients_list_from_post,
    create_recipeingredients,
    update_tags,
    prepare_context_from_post,
    prepare_context_from_recipe_instance,
)


def recipe(request, recipe_id):
    recipe_instance = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe_instance.recipeingredient_set.all().select_related(
        'ingredient'
    )
    tags = recipe_instance.tags.values_list('slug', flat=True)
    return render(
        request,
        'singlePage.html',
        {'recipe': recipe_instance, 'ingredients': ingredients, 'tags': tags}
    )


@login_required
def new_recipe(request):
    if request.method == 'POST':
        recipe_instance = Recipe(author=request.user)
        form = RecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe_instance
        )
        valid_ingredients, invalid_ingredients = validate_ingredients_list_from_post(
            request
        )

        if form.is_valid() and not invalid_ingredients:
            with transaction.atomic():
                form.save()
                create_recipeingredients(recipe_instance, valid_ingredients)
                update_tags(request, recipe_instance)
                #  TODO: Перенаправлять на index
            return redirect('password_change')
        context = prepare_context_from_post(
            request, form, valid_ingredients, invalid_ingredients
        )
        return render(request, 'formRecipe.html', context)
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe_instance = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe_instance.author:
        # TODO: Перенаправлять на index
        return redirect('password_change')

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe_instance
    )
    if request.method == 'POST':
        valid_ingredients, invalid_ingredients = validate_ingredients_list_from_post(
            request
        )
        if form.is_valid() and not invalid_ingredients:
            with transaction.atomic():
                form.save()
                create_recipeingredients(recipe_instance, valid_ingredients)
                update_tags(request, recipe_instance)
                #  TODO: Перенаправлять на index
                return redirect('password_change')
        context = prepare_context_from_post(
            request, form, valid_ingredients, invalid_ingredients
        )
        return render(request, 'formChangeRecipe.html', context)
    context = prepare_context_from_recipe_instance(recipe_instance, form)
    return render(request, 'formChangeRecipe.html', context)


def get_ingredients(request):
    query_text = request.GET.get('query', None)
    search_query = Ingredient.objects.filter(title__istartswith=query_text)[:8]
    results = [
        {"title": result.title, "dimension": result.measurement.title}
        for result in search_query
    ]
    result_json = json.dumps(results)
    print(result_json)
    return HttpResponse(result_json, content_type='application/json')
