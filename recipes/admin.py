from django.contrib import admin

from recipes.models import (
    Recipe,
    Ingredient,
    Measurement,
    Tag,
    BookmarkRecipe,
    ShoppingList,
    RecipeIngredient,
    Follow,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "created_at", "author")
    search_fields = ("title", "author__username")
    list_filter = ("created_at",)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "measurement")
    search_fields = ("title",)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Measurement)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(BookmarkRecipe)
admin.site.register(ShoppingList)
admin.site.register(RecipeIngredient)
