from django.db import models
from accounts.models import Absmodel,User,SoftDeleteManager,GENDER_CHOICES
from accounts.utils import MobileNumberField
# from doctor.models import Education
from datetime import date
# Create your models here.






class WorkExperience(models.Model):
    st=models.ForeignKey('StudentProfile',on_delete=models.CASCADE,blank=True, null=True,related_name='work_experience')
    company = models.CharField(max_length=255,blank=True, null=True)
    position = models.CharField(max_length=2355,blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    paid=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
class Education(models.Model):
    st=models.ForeignKey('StudentProfile',on_delete=models.CASCADE,blank=True, null=True,related_name='education')
    institute = models.CharField(max_length=250,blank=True, null=True)
    degree = models.CharField(max_length=55,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_graduated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.degree} from {self.institute}"

class StudentProfile(Absmodel):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True,limit_choices_to={'role':'student'})
    
    profpic = models.ImageField(upload_to='student_profile_images', default='/images/default.jpg')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(null=True)
    phone = MobileNumberField(null=True)
    address = models.CharField(max_length=100, null=True)
    major = models.CharField(max_length=100, null=True)
    profemail=models.EmailField(null=True,blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    biography=models.CharField(max_length=250, null=True, blank=True)
    fblink=models.URLField(null=True, blank=True)
    instalink=models.URLField(null=True, blank=True)
    youtubelink=models.URLField(null=True, blank=True)
    websitelink=models.URLField(null=True, blank=True)
    twitter=models.URLField(null=True, blank=True)
    linkedin=models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SoftDeleteManager()
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        else:
            return None

    def __str__(self):
        return f'{self.name.first_name} {self.name.last_name}'
    
# class Education(models.Model):
#     student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,blank=True, null=True,related_name='education')
#     institute = models.CharField(max_length=100,blank=True, null=True)
#     degree = models.CharField(max_length=55,blank=True, null=True)
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     is_graduated = models.BooleanField(default=False)
    
#     def __str__(self):
#         return f"{self.degree} from {self.institute}"
    

# class Major(models.Model):
#     student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,blank=True, null=True,related_name='major')
#     name = models.CharField(max_length=55, default='mbbs',)