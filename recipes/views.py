import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import Recipe, Ingredient, Follow, User, BookmarkRecipe, ShoppingList
from .utils import (
    validate_ingredients_list_from_post,
    create_recipeingredients,
    update_tags,
    prepare_context_from_post,
    prepare_context_from_recipe_instance,
)


def index(request):
    recipes = (
        Recipe.objects.select_related('author')
        .prefetch_related('tags')
        .order_by('-created_at')
    )
    tags = request.GET.get('tag', None)
    if tags:
        recipes = recipes.filter(tags__slug__in=tags.split('_'))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "index.html", {'page': page, 'paginator': paginator, 'tags': tags}
    )


def author(request, author_id):
    author = get_object_or_404(User, id=author_id)
    recipes = (
        Recipe.objects.select_related('author')
        .prefetch_related('tags')
        .filter(author=author)
        .order_by('-created_at')
    )
    tags = request.GET.get('tag', None)
    if tags:
        recipes = recipes.filter(tags__slug__in=tags.split('_'))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "authorRecipe.html",
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'author': author,
        },
    )


@login_required
def my_bookmarks(request):
    recipes = (
        Recipe.objects.filter(bookmarked__user=request.user)
        .select_related('author')
        .prefetch_related('tags')
        .order_by('-created_at')
    )
    tags = request.GET.get('tag', None)
    if tags:
        recipes = recipes.filter(tags__slug__in=tags.split('_'))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "favorite.html",
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
        },
    )


@login_required
def my_subscriptions(request):
    authors = (
        User.objects.filter(following__user=request.user)
        .prefetch_related('recipes')
        .annotate(recipes_count=Count('recipes') - 3)
    )
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "myFollow.html", {'page': page, 'paginator': paginator})


def recipe(request, recipe_id):
    recipe_instance = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe_instance.recipeingredient_set.all().select_related(
        'ingredient'
    )
    tags = recipe_instance.tags.values_list('slug', flat=True)
    return render(
        request,
        'singlePage.html',
        {
            'recipe': recipe_instance,
            'ingredients': ingredients,
            'tags': tags,
        },
    )


@login_required
def new_recipe(request):
    if not request.method == 'POST':
        form = RecipeForm()
        return render(request, 'formRecipe.html', {'form': form})
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
        return redirect('index')
    context = prepare_context_from_post(
        request, form, valid_ingredients, invalid_ingredients
    )
    return render(request, 'formRecipe.html', context)


@login_required
def edit_recipe(request, recipe_id):
    recipe_instance = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe_instance.author:
        return redirect('index')

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
                return redirect('index')
        context = prepare_context_from_post(
            request, form, valid_ingredients, invalid_ingredients
        )
        return render(request, 'formRecipe.html', context)
    context = prepare_context_from_recipe_instance(recipe_instance, form)
    return render(request, 'formRecipe.html', context)


@login_required
def get_ingredients(request):
    query_text = request.GET.get('query', None)
    search_query = Ingredient.objects.filter(title__istartswith=query_text)[:8]
    results = [
        {"title": result.title, "dimension": result.measurement.title}
        for result in search_query
    ]
    result_json = json.dumps(results)
    return HttpResponse(result_json, content_type='application/json')


@login_required
@require_http_methods(['POST', 'DELETE'])
def subscriptions(request, author_id=None):
    if request.method == 'POST':
        body = json.loads(request.body)
        author_id = body['id']
        author = get_object_or_404(User, id=author_id)

        subscribe, created = Follow.objects.get_or_create(
            user=request.user, author=author
        )

        result = {'success': True} if created else {'success': False}
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')
    else:
        author = get_object_or_404(User, id=author_id)
        subscription = Follow.objects.get(user=request.user, author=author).delete()

        result = {'success': True} if subscription else {'success': False}
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')


@login_required
@require_http_methods(['POST', 'DELETE'])
def favorites(request, recipe_id=None):
    if request.method == 'POST':
        body = json.loads(request.body)
        recipe_id = body['id']
        bookmark_recipe = get_object_or_404(Recipe, id=recipe_id)

        bookmark, created = BookmarkRecipe.objects.get_or_create(
            user=request.user, recipe=bookmark_recipe
        )

        result = {'success': True} if created else {'success': False}
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')

    if request.method == 'DELETE':
        bookmark_recipe = get_object_or_404(Recipe, id=recipe_id)
        bookmark = BookmarkRecipe.objects.get(
            user=request.user, recipe=bookmark_recipe
        ).delete()

        result = {'success': True} if bookmark else {'success': False}
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')


@login_required
@require_http_methods(['GET', 'POST', 'DELETE'])
def oh_my_purchpurchases(request, recipe_id=None):
    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        body = json.loads(request.body)
        recipe_id = body['id']
        try:
            recipe_to_buy = get_object_or_404(Recipe, id=recipe_id)
            shopping_list.recipes.add(recipe_to_buy)
            result = {'success': True}
        except Exception:
            result = {'success': False}

        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')

    elif request.method == 'DELETE':
        try:
            recipe_to_remove = get_object_or_404(Recipe, id=recipe_id)
            shopping_list.recipes.remove(recipe_to_remove)
            result = {'success': True}
        except Exception:
            result = {'success': False}

        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')

    recipes = Recipe.objects.filter(recipe_to_buy__user=request.user)
    return render(
        request,
        "shopList.html",
        {
            'recipes': recipes,
        },
    )


@login_required
def generate_pdf(request):
    recipes = Recipe.objects.filter(recipe_to_buy__user=request.user)

    ingredients = defaultdict(int)
    for recipe in recipes:
        for ingredient in recipe.recipeingredient_set.all():
            ingredients[ingredient.ingredient] += ingredient.amount

    output = ['Список покупок:\n']
    for ingredient, total in ingredients.items():
        output.append(f'{ingredient}: {total} {ingredient.measurement.title}')

    filename = "ShoppingList.txt"
    content = '\n'.join(output)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
