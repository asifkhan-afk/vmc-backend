# Generated by Django 4.2 on 2023-06-05 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_message_created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 5, 12, 9, 3, 473502), max_length=255),
        ),
    ]