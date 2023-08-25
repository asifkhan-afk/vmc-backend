from rest_framework import serializers

from student.serilizers import StudentProfileSerilizer
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

class SpecialitySerilizer(serializers.ModelSerializer):
    class Meta:
        model=Speciality
        fields='__all__'
        

class DrProfileSerilizer(serializers.ModelSerializer):
    
    name=UserSerializer()
    education = EducationSerilizer(many=True, read_only=True)
    specialities = SpecialitySerilizer(many=True, read_only=True)
    work_experience=WorkxperienceSerilizer(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    
    class Meta:
        model =DrProfile
        fields='__all__'
        # fields=['id','name','profile_image','qualifications','specialities','work_email',"address","work_address","Consultancy_Charge","phone","is_deleted"]
    def to_representation(self, instance):
       
        self.fields['specialities'] = SpecialitySerilizer(many=True, read_only=True)
        return super().to_representation(instance)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('name__post_set')

class GetSpecialitySerilizer(serializers.ModelSerializer):
    doctor=DrProfileSerilizer(read_only=True)
    class Meta:
        model=Speciality
        fields='__all__'

class ResearchPostSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model=Research
        fields='__all__'






class ResearchSerilizer(serializers.ModelSerializer):
    doctor=DrProfileSerilizer(read_only=True)
    class Meta:
        model=Research
        fields = ('id', 'doctor', 'title','description', 'skills_required', 'application_deadline', 'posted_at', 'is_active')
        def get_is_active(self, obj):
         return obj.application_deadline >= timezone.now()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        posted_at = instance.posted_at
        application_deadline=instance.application_deadline

        # Format the time and date separately
        time = posted_at.strftime("%I:%M %p")  # Format time as 12-hour clock
        date = posted_at.strftime("%B %d, %Y")  # Format date as Month day, Year
        representation['posted_at'] = {
            'time': time,
            'date': date,
        }
        time = application_deadline.strftime("%I:%M %p")  # Format time as 12-hour clock
        date = application_deadline.strftime("%B %d, %Y")  # Format date as Month day, Year
        representation['application_deadline'] = {
            'time': time,
            'date': date,
        }

        return representation
    


class ResearchApplySerializer(serializers.ModelSerializer):
    student=StudentProfileSerilizer(read_only=True)
    class Meta:
        model = ResearchApply
        fields = ['id', 'research', 'student', 'status', 'cover_letter', 'resume', 'applied_at']
class ResearchApplyPOSTSerializer(serializers.ModelSerializer):
    # student=StudentProfileSerilizer()
    class Meta:
        model = ResearchApply
        fields = ['id', 'research', 'student', 'status', 'cover_letter', 'resume', 'applied_at']

    def create(self, validated_data):
        print("Request data:", validated_data)
        return super().create(validated_data)

class StudentResearchApplySerializer(serializers.ModelSerializer):
    student=StudentProfileSerilizer(read_only=True)
    research=ResearchSerilizer(read_only=True)
    class Meta:
        model = ResearchApply
        fields = ['id', 'research', 'student', 'status', 'cover_letter', 'resume', 'applied_at']