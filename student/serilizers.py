from rest_framework import serializers
# from doctor.serilizers import QualificationSerilizer
from .models import *
from accounts.serilizers import UserSerializer



class EducationSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Education
        fields='__all__'

class WorkxperienceSerilizer(serializers.ModelSerializer):
    class Meta:
        model=WorkExperience
        fields='__all__'

class StudentProfileSerilizer(serializers.ModelSerializer):
    name=UserSerializer(read_only=True)
    education = EducationSerilizer(many=True, read_only=True)
  
    work_experience=WorkxperienceSerilizer(many=True, read_only=True)
    # Qualification=QualificationSerilizer(many=True,read_only=True)
    class Meta:
        model=StudentProfile
        fields='__all__'