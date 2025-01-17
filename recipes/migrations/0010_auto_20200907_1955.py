# Generated by Django 3.1.1 on 2020-09-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20200907_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, related_name='recipes', through='recipes.RecipeIngredient', to='recipes.Ingredient'),
        ),
    ]
