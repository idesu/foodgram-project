# Generated by Django 3.1.1 on 2020-09-05 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredients',
            name='measurement',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='ingredients', to='recipes.measurement'),
        ),
    ]
