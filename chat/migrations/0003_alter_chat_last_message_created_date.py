# Generated by Django 4.2.2 on 2023-06-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chat_last_message_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_message_created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]