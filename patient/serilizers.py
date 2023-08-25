from rest_framework import serializers
from .models import *
from accounts.serilizers import UserSerializer

class PatientProfileSerilizer(serializers.ModelSerializer):
    name=UserSerializer()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        if obj.date_of_birth:
            today = date.today()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
    class Meta:
        model=PatientProfile
        fields='__all__'

