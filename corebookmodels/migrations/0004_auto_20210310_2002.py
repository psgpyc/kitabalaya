# Generated by Django 3.0.3 on 2021-03-10 14:17

import corebookmodels.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corebookmodels', '0003_auto_20210310_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcategory',
            name='belongs_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(corebookmodels.models.get_sentinel_book_category), related_name='main_category', to='corebookmodels.BookMainCategory'),
        ),
        migrations.AlterField(
            model_name='bookmaincategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
