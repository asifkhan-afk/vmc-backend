# Generated by Django 4.2 on 2023-07-30 04:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0008_remove_appointment_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='scheduled_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
