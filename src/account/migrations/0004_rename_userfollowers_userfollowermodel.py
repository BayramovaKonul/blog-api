# Generated by Django 5.1 on 2025-01-01 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userfollowers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollowers',
            new_name='UserFollowerModel',
        ),
    ]
