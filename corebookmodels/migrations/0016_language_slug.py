# Generated by Django 3.0.3 on 2021-07-27 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corebookmodels', '0015_genre_belongs_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
