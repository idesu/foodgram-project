# Generated by Django 3.1.1 on 2020-09-06 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20200905_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='slug',
        ),
        migrations.AlterField(
            model_name='measurement',
            name='title',
            field=models.CharField(max_length=30, unique=True, verbose_name='Название меры весов'),
        ),
    ]
