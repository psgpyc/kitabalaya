# Generated by Django 3.0.3 on 2021-07-25 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corebookmodels', '0013_delete_bookratingmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
