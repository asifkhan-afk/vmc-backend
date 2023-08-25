from django.db import models
from accounts.models import User
from doctor.models import DrProfile
from patient.models import PatientProfile
from hospital.models import HospitalProfile

# Create your models here.

class Appointment(models.Model):
    APPOINTMENT_TYPE = (
        ("d", "Doctor"),
        ("p", "Patient"),
    )
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('expired','Expired'),
        ('completed', 'Completed'),
    ]
    VISIT_TYPE=[
        ('new','New'),
        ('revisit',"Re-Visit")
    ]
    
    # appointment_type = models.CharField(max_length=1, choices=APPOINTMENT_TYPE)
    visit_type=models.CharField(max_length=9,choices=VISIT_TYPE,default='new')
    doctor = models.ForeignKey(DrProfile, related_name="doctor_appointments", on_delete=models.CASCADE, null=True, blank=True)
    hospital=models.ForeignKey(HospitalProfile,related_name="hs_appointments", on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(PatientProfile, related_name="patient_appointments", on_delete=models.CASCADE, null=True, blank=True)
    scheduled_time= models.TimeField()
    scheduled_date=models.DateField()
    
    # duration = models.PositiveSmallIntegerField(default=15) # duration of appointment in minutes
    reason=models.CharField(max_length=80)
    history=models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f' Dr.{self.doctor}|{self.hospital}  pt {self.patient} {self.reason}'
    class Meta:
        ordering = ['-created_at']