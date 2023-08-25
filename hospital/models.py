from django.utils import timezone
from django.db import models
from accounts.models import Absmodel,User,SoftDeleteManager,GENDER_CHOICES
from accounts.utils import MobileNumberField
from doctor.models import DrProfile
from student.models import StudentProfile
from django.db.models import Q
# Create your models here.




class HospitalProfile(Absmodel):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profpic=models.ImageField(upload_to='profilepics',default='/images/default.jpg')
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mobile = MobileNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    

    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()

    def __str__(self):
        return f'{self.name.first_name}  {self.name.last_name}'
    



class Gallery(models.Model):
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='hospitalgallery')
    caption = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        if self.caption:
            return self.caption
        else:
            return 'gallery image'


class Job(Absmodel):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary','Temporary'),
        ('volinteer','Volinteer'),
        ('internship','Internship'),
        ('other','Other'),
    ]
    WORKPLACELOCATION = [
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]
    

    hospital = models.ForeignKey('HospitalProfile', on_delete=models.CASCADE, related_name='jobs')
    position = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    workplace=models.CharField(max_length=20, choices=WORKPLACELOCATION)
    description = models.TextField(null=True,blank=True)
    qualification = models.TextField(null=True,blank=True)
    requirements = models.TextField()
    start_salary = models.PositiveIntegerField(null=True,blank=True)
    end_salary = models.PositiveIntegerField(null=True,blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.position
    class Meta:
        ordering = ['-published_at']


    @property
    def is_active(self):
        return self.application_deadline >= timezone.now()
    
class Apply(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    doctor = models.ForeignKey(DrProfile, on_delete=models.CASCADE,null=True,blank=True,related_name="dr_applies")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,null=True,blank=True,related_name="st_applies")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(max_length=1000)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor}|{self.student} - {self.job.position} Application"
    
    class Meta:
        ordering=['-applied_at']
    


class Affiliated_doctors(models.Model):
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE, related_name='affiliated_dr')
    doctor = models.ForeignKey(DrProfile, on_delete=models.CASCADE, related_name='affiliated_hs',null=True, default=None)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,null=True,blank=True,related_name="affiliated_hs")
    joined_from = models.DateField(auto_now_add=True)
    position=models.CharField(max_length=50,default=None)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        doctor_name = self.doctor.name.first_name if self.doctor else ''
        student_name = self.student.name.first_name if self.student else ''
        return f"HOSPITAL: {self.hospital.name.first_name} DOCTOR: {doctor_name} STUDENT: {student_name}"
    class Meta:
        unique_together = ['student','position','hospital', 'doctor']







class HospitalDepartment(models.Model):
    name = models.CharField(max_length=255)
    dptphoto = models.ImageField(upload_to='hospitalgallery',default='/images/defaultdepartment.PNG')
    description = models.TextField(null=True)
    hospital = models.ForeignKey('HospitalProfile', on_delete=models.CASCADE, related_name='departments')




class HospitalServices(models.Model):
    name = models.CharField(max_length=255)
    srphoto = models.ImageField(upload_to='hospitalservices',null=True,blank=True)
    description = models.TextField(null=True)
    hospital = models.ForeignKey('HospitalProfile', on_delete=models.CASCADE, related_name='services')



    
