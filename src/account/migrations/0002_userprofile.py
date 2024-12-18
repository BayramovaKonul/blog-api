# Generated by Django 5.1 on 2024-12-15 12:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateTimeField(blank=True, null=True, verbose_name='birthday')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='media/user_profile_pictures/', verbose_name='profile_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User_profile',
                'verbose_name_plural': 'User_profiles',
                'db_table': 'user_profile',
            },
        ),
    ]
