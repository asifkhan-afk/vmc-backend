# Generated by Django 4.2 on 2023-07-01 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_followers',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='user',
            new_name='follower',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'following'), name='unique_followers'),
        ),
    ]