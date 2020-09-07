from django.urls import path

from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
]
