# Generated by Django 4.2 on 2023-07-30 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0024_drprofile_max_appointment_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drprofile',
            name='working_hours_end',
            field=models.TimeField(default=datetime.time(12, 0)),
        ),
        migrations.AlterField(
            model_name='drprofile',
            name='working_hours_start',
            field=models.TimeField(default=datetime.time(6, 0)),
        ),
    ]
