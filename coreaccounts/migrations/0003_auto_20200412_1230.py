# Generated by Django 3.0.3 on 2020-04-12 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreaccounts', '0002_activateemail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activateemail',
            old_name='is_active',
            new_name='activated',
        ),
        migrations.RemoveField(
            model_name='activateemail',
            name='expires',
        ),
    ]