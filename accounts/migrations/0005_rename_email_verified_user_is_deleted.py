# Generated by Django 4.2 on 2023-07-18 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_verified',
            new_name='is_deleted',
        ),
    ]
