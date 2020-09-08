from django.urls import path

from . import views


urlpatterns = [
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscriptions/<int:author_id>/', views.subscriptions, name='remove_subscription'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:recipe_id>/', views.favorites, name='remove_favorite'),
    path('', views.index, name='index'),
]
