from django.core.exceptions import ValidationError

from recipes.models import Tag, RecipeIngredient, Ingredient


def prepare_context_from_recipe_instance(recipe_instance, form):
    ingredients_list = []
    for idx, recipeingredient in enumerate(recipe_instance.recipeingredient_set.all()):
        ingredients_list.append(
            {
                'id': idx + 1,
                'title': recipeingredient.ingredient.title,
                'amount': recipeingredient.amount,
                'units': recipeingredient.ingredient.measurement.title,
            }
        )
    tags = {
        tag: 'on'
        for tag in recipe_instance.tags.all().values_list('title', flat=True)
    }

    return {'form': form, 'valid_ingredients': ingredients_list, 'tags': tags, 'ingredients_count': len(ingredients_list)+1}


def prepare_context_from_post(request, form, valid_ingredients, invalid_ingredients) -> dict:
    valid = []
    for idx, ingredient in enumerate(valid_ingredients):
        valid.append(
            {
                'id': idx + 1,
                'title': ingredient['ingredient'].title,
                'amount': ingredient['amount'],
                'units': ingredient['ingredient'].measurement.title,
            }
        )

    tags = {
        tag: request.POST[tag]
        for tag in Tag.objects.all().values_list('title', flat=True)
        if tag in request.POST
    }

    if invalid_ingredients:
        invalid_ingredients = ', '.join(invalid_ingredients)
        form.add_error(
            field='ingredients',
            error=ValidationError(
                f'Ингредиентов {invalid_ingredients} не существует.'
            )
        )
    return {'form': form, 'valid_ingredients': valid, 'tags': tags, 'ingredients_count': len(valid)+1}


def validate_ingredients_list_from_post(request) -> tuple:
    """функция обрабатывает список ингредиентов с фронтенда и валидирует их наличие в базе."""

    invalid_ingredients = []
    valid_ingredients_data = []
    for key, val in request.POST.items():
        if key.startswith('nameIngredient'):
            ingredient_number = key.strip('nameIngredient_')
            #  Может и не быть в случае с "по вкусу"
            ingredient_amount = request.POST.get(
                f'valueIngredient_{ingredient_number}', None
            )
            ingredient_amount = int(ingredient_amount) if ingredient_amount else None
            try:
                ingredient = Ingredient.objects.get(title=val)
                valid_ingredients_data.append(
                    {'ingredient': ingredient, 'amount': ingredient_amount}
                )
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
