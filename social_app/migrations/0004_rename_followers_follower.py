# Generated by Django 5.0.6 on 2024-05-16 18:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0003_followers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
    ]
