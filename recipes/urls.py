from django.urls import path

from . import views


urlpatterns = [
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('user/<int:author_id>/', views.author, name='author'),
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
    path('my_subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('my_bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path(
        'subscriptions/<int:author_id>/',
        views.subscriptions,
        name='remove_subscription',
    ),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:recipe_id>/', views.favorites, name='remove_favorite'),
    path('purchases/', views.oh_my_purchpurchases, name='purchases'),
    path(
        'purchases/<int:recipe_id>/', views.oh_my_purchpurchases, name='remove_purchase'
    ),
    path('generate_shop_list_pdf/', views.generate_pdf, name='generate_pdf'),
    path('', views.index, name='index'),
]
