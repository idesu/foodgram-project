from recipes.models import Recipe


def shopping_count(request):
    if not request.user.is_anonymous:
        recipes_count = Recipe.objects.filter(
            recipe_to_buy__user=request.user
        ).count()
    else:
        recipes_count = ''
    return {"shopping_list_count": recipes_count}
