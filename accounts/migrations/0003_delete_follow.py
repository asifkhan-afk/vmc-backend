# Generated by Django 4.2 on 2023-05-09 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_follow_follow_unique_followers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
