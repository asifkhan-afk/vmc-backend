# Generated by Django 4.2 on 2023-05-13 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0020_affiliated_doctors_doctor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affiliated_doctors',
            name='doctor',
        ),
        migrations.AlterField(
            model_name='affiliated_doctors',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliated_dr', to='hospital.hospitalprofile'),
        ),
    ]
