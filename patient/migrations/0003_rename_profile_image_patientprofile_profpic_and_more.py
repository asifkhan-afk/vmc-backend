# Generated by Django 4.2 on 2023-05-29 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patientprofile_profile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientprofile',
            old_name='profile_image',
            new_name='profpic',
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='biography',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='fblink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='instalink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='websitelink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='youtubelink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
