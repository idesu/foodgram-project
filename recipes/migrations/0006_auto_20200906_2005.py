# Generated by Django 3.1.1 on 2020-09-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20200906_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='Теги', to='recipes.Tag'),
        ),
    ]
