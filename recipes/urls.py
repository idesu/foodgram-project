from django.urls import path

from . import views


urlpatterns = [
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('user/<int:author_id>/', views.author, name='author'),
    path('my_subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('my_bookmarks/', views.my_bookmarks, name='my_bookmarks'),

    path('api/ingredients/', views.get_ingredients, name='get_ingredients'),
    path('api/favorites/', views.favorites, name='favorites'),
    path('api/favorites/<int:recipe_id>/', views.favorites, name='remove_favorite'),
    path('api/delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('api/purchases/', views.oh_my_purchpurchases, name='purchases'),
    path(
        'api/purchases/<int:recipe_id>/', views.oh_my_purchpurchases, name='remove_purchase'
    ),
    path('api/subscriptions/', views.subscriptions, name='subscriptions'),
    path(
        'api/subscriptions/<int:author_id>/',
        views.subscriptions,
        name='remove_subscription',
    ),


    path('api/generate_shop_list_pdf/', views.generate_pdf, name='generate_pdf'),
    path('', views.index, name='index'),
]
