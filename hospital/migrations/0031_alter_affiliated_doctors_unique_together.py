# Generated by Django 4.2 on 2023-07-17 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0021_alter_researchapply_student'),
        ('hospital', '0030_rename_positoin_affiliated_doctors_position'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='affiliated_doctors',
            unique_together={('position', 'doctor')},
        ),
    ]