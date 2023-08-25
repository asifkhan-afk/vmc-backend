# Generated by Django 4.2 on 2023-05-13 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_drprofile_affiliated_with_and_more'),
        ('hospital', '0021_remove_affiliated_doctors_doctor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliated_doctors',
            name='doctor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affiliated_hs', to='doctor.drprofile'),
        ),
    ]
