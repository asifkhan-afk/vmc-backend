# Generated by Django 4.2 on 2023-04-05 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_hospitalprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]