from django.db import models
from accounts.models import Absmodel,User,SoftDeleteManager,GENDER_CHOICES
from accounts.utils import MobileNumberField
from student.models import StudentProfile
from django.utils import timezone
from django.db import models
import datetime

class WorkExperience(models.Model):
    dr=models.ForeignKey('DrProfile',on_delete=models.CASCADE,blank=True, null=True,related_name='work_experience')
    company = models.CharField(max_length=255,blank=True, null=True)
    position = models.CharField(max_length=255,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
class Education(models.Model):
    dr=models.ForeignKey('DrProfile',on_delete=models.CASCADE,blank=True, null=True,related_name='education')
    institute = models.CharField(max_length=100,blank=True, null=True)
    degree = models.CharField(max_length=55,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_graduated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.degree} from {self.institute}"


class Speciality(models.Model):
    dr=models.ForeignKey('DrProfile',on_delete=models.CASCADE,blank=True, null=True,related_name='specialities')
    name = models.CharField(max_length=55, default='cardio',)
    
    def __str__(self):
        return self.name
    

class DrProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True, limit_choices_to={'is_active': True, 'role': 'doctor'})
    profpic = models.ImageField(upload_to='dr_profile_pics', default='/images/default.jpg')
    language = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=1)
    profemail=models.EmailField(null=True,blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    work_address = models.CharField(max_length=100, null=True, blank=True)
    working_hours_start = models.TimeField( default=datetime.time(6, 0))
    working_hours_end = models.TimeField(default=datetime.time(12, 0))
    max_appointment_time = models.PositiveIntegerField(default=30) 
    Consultancy_Charge = models.PositiveIntegerField(null=True)
    biography=models.CharField(max_length=250, null=True, blank=True)
    phone = MobileNumberField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fblink=models.URLField(null=True, blank=True)
    instalink=models.URLField(null=True, blank=True)
    youtubelink=models.URLField(null=True, blank=True)
    websitelink=models.URLField(null=True, blank=True)
    twitter=models.URLField(null=True, blank=True)
    linkedin=models.URLField(null=True, blank=True)
    is_deleted=models.BooleanField(default=False)
    objects = SoftDeleteManager()

    def __str__(self):
        return f'{self.name.first_name} {self.name.last_name}'

class Research(models.Model):
    doctor = models.ForeignKey('DrProfile', on_delete=models.CASCADE, related_name='research')
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.CharField(max_length=255)
    application_deadline = models.DateTimeField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-posted_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        return self.application_deadline >= timezone.now()

class ResearchApply(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,related_name="research_application")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(max_length=1000)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.research.title} Application"
    class Meta:
        ordering = ['-applied_at']
    