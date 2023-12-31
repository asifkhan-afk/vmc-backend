# Generated by Django 4.2 on 2023-07-29 01:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0032_alter_affiliated_doctors_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='close_date',
        ),
        migrations.RemoveField(
            model_name='job',
            name='open_date',
        ),
        migrations.AddField(
            model_name='job',
            name='application_deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
