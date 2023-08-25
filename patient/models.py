from django.db import models
from accounts.models import Absmodel,User,SoftDeleteManager,GENDER_CHOICES
from accounts.utils import MobileNumberField
from datetime import date

  
# Create your models here.
class PatientProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profpic = models.ImageField(upload_to='patient_profile_images/', default='images/default.jpg')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    language=models.CharField(max_length=66,null=True,blank=True)
    date_of_birth = models.DateField(null=True)
    phone = MobileNumberField(null=True,blank=True)
    fblink=models.URLField(null=True, blank=True)
    instalink=models.URLField(null=True, blank=True)
    profemail=models.EmailField(null=True,blank=True)
    twitter=models.URLField(null=True, blank=True)
    biography=models.CharField(max_length=250, null=True, blank=True)
    is_deleted=models.BooleanField(default=False)
    address = models.CharField(max_length=100, null=True)
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
    