# Generated by Django 4.2 on 2023-07-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_remove_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='notification',
            name='assignment_quiz_meeting_class_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='message_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='message_type',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='teacher_user_id',
        ),
        migrations.AddField(
            model_name='notification',
            name='deleted_for',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read_by',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='receiver_id',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
    ]