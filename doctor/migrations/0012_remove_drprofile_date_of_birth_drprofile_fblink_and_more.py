# Generated by Django 4.2 on 2023-05-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0011_drprofile_biography'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drprofile',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='drprofile',
            name='fblink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='drprofile',
            name='instalink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='drprofile',
            name='websitelink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='drprofile',
            name='youtubelink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
