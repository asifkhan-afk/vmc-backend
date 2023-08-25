# Generated by Django 4.2 on 2023-07-22 02:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_email_verified_user_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=55, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')]),
        ),
    ]
