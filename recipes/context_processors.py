from recipes.models import Recipe, Tag


def shopping_count(request):
    if request.user.is_authenticated:
        recipes_count = Recipe.objects.filter(
            recipe_to_buy__user=request.user
        ).count()
    else:
        recipes_count = ''
    return {"shopping_list_count": recipes_count}


def all_tags(request):
    all_tags = Tag.objects.all()
    return {'all_tags': all_tags}
