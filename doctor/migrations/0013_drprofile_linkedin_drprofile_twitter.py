# Generated by Django 4.2 on 2023-05-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0012_remove_drprofile_date_of_birth_drprofile_fblink_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drprofile',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='drprofile',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
