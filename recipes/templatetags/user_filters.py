from django import template

from recipes.models import BookmarkRecipe

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def does_recipe_in_bookmarks(recipe, user) -> True:
    """Returns True if a recipe in bookmarks.
    Usage::
        {% if recipe|does_recipe_in_bookmarks:user %}
        ...
        {% endif %}
    """
    return BookmarkRecipe.objects.filter(user=user, recipe=recipe).exists()
