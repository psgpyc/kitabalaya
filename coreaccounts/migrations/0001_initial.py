# Generated by Django 3.0.3 on 2020-03-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='User Email')),
                ('phone_number', models.CharField(max_length=14, unique=True, verbose_name='Phone Number')),
                ('full_name', models.CharField(max_length=100, verbose_name="USer's Full Name")),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('NB', 'Non Binary'), ('UD', 'Prefer not to say')], default='UD', max_length=2, null=True, verbose_name='Gender')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, editable=False)),
                ('is_superuser', models.BooleanField(default=False, editable=False)),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Email Confirmed?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
