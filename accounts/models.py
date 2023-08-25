from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .utils import MobileNumberField
from datetime import date


alphabet_validator = RegexValidator(
    r'^[a-zA-Z]+$',
    'Only alphabetic characters are allowed.'
)

# #custom manager for soft delete
class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        return super().get_queryset()

    def deleted_only(self):
        return super().get_queryset().filter(is_deleted=True)
    

# abstract Model of custom manager
class Absmodel(models.Model):
    is_deleted=models.BooleanField(default=False)   
    objects=SoftDeleteManager()
    
    
    class Meta:
        abstract=True



class CustomUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    def all_objects(self):
        return super().get_queryset()
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_deleted=True
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

#MAIN USER 
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

ROLE = (
    ("doctor", "Doctor"),
    ("student", "Student"),
    ("hospital", "Hospital"),
    ("patient", "Patient"),
)
class User(AbstractUser):
    username = None
    profilepic=models.ImageField(upload_to='dr_profile_pics',null=True,blank=True,default='/images/default.jpg')
    first_name = models.CharField(max_length=55, validators=[alphabet_validator])
    last_name = models.CharField(max_length=35, null=True, validators=[alphabet_validator])
    created=models.DateTimeField(auto_now_add=True)
    email = models.EmailField(_('email address'), unique=True)
    is_deleted = models.BooleanField(default=False)
    role = models.CharField(
        max_length = 8,
        choices = ROLE,
        default = 'doctor'
        )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.email}'
    
    def get_post_count(self):
        return self.userposts.count()
    
    def get_followers(self):
        return self.following.all()

    def get_following(self):
        return self.follower.all()
    
    def get_follower_count(self):
        return self.following.count()
    
    def get_following_count(self):
        return self.follower.count()
    
    def get_userlikes(self):
        return self.likedposts.count()
   








