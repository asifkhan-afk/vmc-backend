# Generated by Django 4.2 on 2023-05-17 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_drprofile_profemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='drprofile',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
