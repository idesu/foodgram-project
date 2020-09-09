from django import template

from recipes.models import BookmarkRecipe

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def does_recipe_in_bookmarks(recipe, user):
    return BookmarkRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def get_tags(request, tag):
    tags = request.GET.get('tag', None)
    tags_list = []
    if not tags:
        tags_list.append(tag)
        return '_'.join(tags_list)
    tags_list = tags.split('_')
    tags_list.append(tag) if tag not in tags_list else tags_list.remove(tag)
    return '_'.join(tags_list)


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
