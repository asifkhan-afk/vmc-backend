from rest_framework import serializers
from .models import *
from accounts.serilizers import UserSerializer
from doctor.serilizers import DrProfileSerilizer
from student.serilizers import StudentProfileSerilizer
from django.utils import timezone
# from doctor.serilizers import DrProfileSerilizer


class HospitalDepartmentSerilizer(serializers.ModelSerializer):
    # hospital=HospitalProfileSerilizer()
    class Meta:
        model=HospitalDepartment
        fields="__all__"

class HospitalServicesSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model=HospitalServices
        fields="__all__"




class HospitalGetProfileSerilizer(serializers.ModelSerializer):
    name=UserSerializer()

    galleries = serializers.SerializerMethodField()
    # departments = HospitalDepartmentSerilizer(many=True )
    services=HospitalServicesSerilizer(many=True)
    
    

    class Meta:
        model=HospitalProfile
        fields="__all__"
        # fields=["id", "name",'galleries', "profpic", "address", "city", "state", "country", "phone_number", "mobile", "email", "website", "description", "created_at", "updated_at", "joined_doctors"]
        # fields=["id", "name",'services','galleries', "profpic", "address", "city", "state", "country", "phone_number", "mobile", "email", "website", "description", "created_at", "updated_at", "afdoctor"]
    def to_representation(self, instance):
        # self.fields['joined_doctors'] = DrProfileSerilizer(many=True, read_only=True)
        self.fields['departments'] = HospitalDepartmentSerilizer(many=True, read_only=True)

        # self.fields['affiliated_dr'] = Afdoctors_serilizer(many=True, read_only=True)
        return super().to_representation(instance)
    
    # def get_interest_doctors(self, obj):
    #     doctors = obj.interested_doctors.prefetch_related('name')
    #     return DrProfileSerilizer(doctors, many=True).data
    
    def get_galleries(self, obj):
        queryset = Gallery.objects.filter(hospital=obj)
        return GallerySerializer(queryset, many=True).data
    
    def get_departments(self, obj):
        queryset = obj.departments.prefetch_related('hospital')
        return HospitalDepartmentSerilizer(queryset, many=True).data
   
class Afdoctors_serilizer(serializers.ModelSerializer):
    doctor=DrProfileSerilizer()
    hospital=HospitalGetProfileSerilizer()
    student=StudentProfileSerilizer()
    class Meta:
        model=Affiliated_doctors
        fields='__all__'

class HospitalProfileSerilizer(serializers.ModelSerializer):
    name=UserSerializer()
    
    
    galleries = serializers.SerializerMethodField()
    # departments = HospitalDepartmentSerilizer(many=True )
    services=HospitalServicesSerilizer(many=True)
    affiliated_dr=Afdoctors_serilizer(many=True)
    

    class Meta:
        model=HospitalProfile
        fields="__all__"
        # fields=["id", "name",'galleries', "profpic", "address", "city", "state", "country", "phone_number", "mobile", "email", "website", "description", "created_at", "updated_at", "joined_doctors"]
        # fields=["id", "name",'services','galleries', "profpic", "address", "city", "state", "country", "phone_number", "mobile", "email", "website", "description", "created_at", "updated_at", "afdoctor"]
    def to_representation(self, instance):
        # self.fields['joined_doctors'] = DrProfileSerilizer(many=True, read_only=True)
        self.fields['departments'] = HospitalDepartmentSerilizer(many=True, read_only=True)

        # self.fields['affiliated_dr'] = Afdoctors_serilizer(many=True, read_only=True)
        return super().to_representation(instance)
    
    # def get_interest_doctors(self, obj):
    #     doctors = obj.interested_doctors.prefetch_related('name')
    #     return DrProfileSerilizer(doctors, many=True).data
    
    def get_galleries(self, obj):
        queryset = Gallery.objects.filter(hospital=obj)
        return GallerySerializer(queryset, many=True).data
    
    def get_departments(self, obj):
        queryset = obj.departments.prefetch_related('hospital')
        return HospitalDepartmentSerilizer(queryset, many=True).data
   
    
class HospitalDepSerilizer(serializers.ModelSerializer):
    hospital=HospitalProfileSerilizer()
    class Meta:
        model=HospitalDepartment
        fields="__all__"
class PostHospitalDepSerilizer(serializers.ModelSerializer):
    class Meta:
        model=HospitalDepartment
        fields="__all__"

class Affiliated_doctors_serilizer(serializers.ModelSerializer):
    hospital=HospitalProfileSerilizer()
    # doctor=DrProfileSerilizer()
    class Meta:
        model=Affiliated_doctors
        fields='__all__'


class HospitalSerSerilizer(serializers.ModelSerializer):
    hospital=HospitalProfileSerilizer()
    class Meta:
        model=HospitalServices
        fields="__all__"
    
# class ApplyGetSerializer(serializers.ModelSerializer):
#     student=StudentProfileSerilizer(read_only=True)
#     doctor=DrProfileSerilizer(read_only=True)
#     class Meta:
#         model = Apply
#         fields = "__all__"


class ApplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = ['id', 'job', 'doctor', 'student', 'status', 'cover_letter', 'resume', 'applied_at']
    
    
# class ApplyGetSerializer(serializers.ModelSerializer):
#     student=StudentProfileSerilizer(read_only=True)
#     doctor=DrProfileSerilizer(read_only=True)
#     class Meta:
#         model = Apply
#         fields = ['id', 'doctor', 'student', 'status', 'cover_letter', 'resume', 'applied_at']

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


    
class HospitalJobySerilizer(serializers.ModelSerializer):
    hospital=HospitalProfileSerilizer(read_only=True)
    class Meta:
        model=Job
        fields= ('id', 'hospital', 'position','job_type','workplace','description','qualification','requirements','start_salary','end_salary','published_at', 'is_active',  'application_deadline')
    

    def get_is_active(self, obj):
         return obj.application_deadline >= timezone.now()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        published_at = instance.published_at
        application_deadline=instance.application_deadline


        # Format the time and date separately
        time = published_at.strftime("%I:%M %p")  # Format time as 12-hour clock
        date = published_at.strftime("%B %d, %Y")  # Format date as Month day, Year
        app_time = application_deadline.strftime("%I:%M %p")  # Format time as 12-hour clock
        app_date = application_deadline.strftime("%B %d, %Y")  # Format date as Month day, Year
        representation['created_at'] = {
            'time': time,
            'date': date,
            
        }
        representation['application_deadline']={
              'time': app_time,
            'date': app_date,
        }


        return representation
    
    

class HospitalPostJobySerilizer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields='__all__'

       

class ApplySerializer(serializers.ModelSerializer):
    job=HospitalJobySerilizer(read_only=True)
    doctor=DrProfileSerilizer(read_only=True)
    student=StudentProfileSerilizer(read_only=True)
    class Meta:
        model = Apply
        fields = ['id', 'job', 'doctor', 'student', 'status', 'cover_letter', 'resume', 'applied_at']


class DrCreationSerilizer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    # password2=serializers.CharField(read_only=True)
    class Meta:
        model=User
        # fields=['email','name','password','password2']
        fields='__all__'
        extra_kwargs={
            'password1':{'write_only':True}
        }
    def validate(self, attrs):
        first_name=attrs.get('first_name')
        password=attrs.get('password')
        password1=attrs.get('password1')
        role='doctor'
        
        
        print("This si passwordssss",password)
        print("This si passwords1",password1)
    
        print("This si first name",first_name)
        print("role",role)

        if len(password)<6:
            raise serializers.ValidationError("Password length must be greater than six")
        if password != password1:
            raise serializers.ValidationError("Password doesn't match hahaha")
        return attrs
    def create(self, validated_data):
        password1 = validated_data.pop('password1', None)
        user= User.objects.create_user(first_name=validated_data['first_name'],
                                       last_name=validated_data['last_name'],
                                       email=validated_data['email'],
                                       password=validated_data['password'],                                    
                                       role=validated_data['role'],                                    
                                    #    is_superuser=validated_data['is_superuser'],                                    
                                    #    is_staff=validated_data['is_staff'],                                    
                                       )
        print("this is user",user)
        return user