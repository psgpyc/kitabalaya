# Generated by Django 3.0.3 on 2020-09-25 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corebookmodels', '0010_auto_20200925_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookratingmodel',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
