# Generated by Django 4.2 on 2023-06-27 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0019_alter_research_options'),
        ('student', '0003_studentprofile_major_workexperience_education'),
        ('hospital', '0024_job_close_date_job_open_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('cover_letter', models.TextField(max_length=1000)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applies', to='doctor.drprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='hospital.job')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applies', to='student.studentprofile')),
            ],
        ),
    ]
