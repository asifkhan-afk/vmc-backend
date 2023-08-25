from rest_framework import serializers
from .models import Appointment
from doctor.serilizers import DrProfileSerilizer
from hospital.serilizers import HospitalProfileSerilizer
from patient.serilizers import PatientProfileSerilizer



class AppointmentSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields='__all__'

class AppointmentGetSerilizer(serializers.ModelSerializer):
    patient=PatientProfileSerilizer(read_only=True)
    doctor=DrProfileSerilizer(read_only=True)
    hospital=HospitalProfileSerilizer(read_only=True)
    class Meta:
        model=Appointment
        fields='__all__'