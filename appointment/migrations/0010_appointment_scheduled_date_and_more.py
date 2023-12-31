# Generated by Django 4.2 on 2023-07-30 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0009_appointment_scheduled_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='scheduled_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='scheduled_time',
            field=models.TimeField(),
        ),
    ]
