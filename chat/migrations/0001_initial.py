# Generated by Django 4.2 on 2023-06-04 08:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message_id', models.CharField(max_length=255)),
                ('last_message_created_date', models.DateTimeField(default=datetime.datetime(2023, 6, 4, 13, 14, 45, 832809), max_length=255)),
                ('total_messages', models.CharField(default=0, max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('reciever_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_reciever', to=settings.AUTH_USER_MODEL)),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('text', 'text'), ('audio', 'audio'), ('image', 'image'), ('video', 'video'), ('file', 'file')], default='text', max_length=30)),
                ('message', models.CharField(default='', max_length=255, null=True)),
                ('read_by', models.CharField(default=[], max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='chat.chat')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('text', 'text'), ('audio', 'audio'), ('image', 'image'), ('video', 'video'), ('file', 'file')], max_length=30)),
                ('attachment', models.FileField(max_length=255, null=True, upload_to='chat')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('chatmessage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage', to='chat.chatmessage')),
            ],
        ),
    ]
