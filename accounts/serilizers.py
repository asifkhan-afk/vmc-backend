from rest_framework import serializers
from .models import *
#rest passowrd
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
#token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from .utils import Util
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from social.models import Like



class LikesSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields = '__all__' 


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['role'] = user.role
        token['email'] = user.email
        return token



class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField(read_only=True)
    follower_count= serializers.SerializerMethodField(read_only=True)
    following_count= serializers.SerializerMethodField(read_only=True)
    userlikes= serializers.SerializerMethodField(read_only=True)
    # likedposts=LikesSerilizer(read_only=True,many=True)
    
    class Meta:
        model = User
        # fields='__all__'
        fields = ['id','likedposts','role','first_name', 'last_name','profilepic','email','post_count','follower_count','following_count' ,'userlikes']

    def get_post_count(self,obj):
        return obj.get_post_count()
    
    def get_follower_count(self,obj):
        return obj.get_follower_count()
    
    def get_following_count(self,obj):
        return obj.get_following_count()
    
    def get_userlikes(self,obj):
        return obj.get_userlikes()
    
    def prefetch_likedposts(self, queryset):
        queryset = queryset.prefetch_related('likedposts')
        return queryset
    
    # def prefetch_userlikes(self, queryset):
    #     queryset = queryset.prefetch_related('userlikes')
    #     return queryset

    





class UserRegSerilizer(serializers.ModelSerializer):
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
        # first_name=attrs.get('first_name')
        password=attrs.get('password')
        password1=attrs.get('password1')
        # role=attrs.get('role')
        
        
        # print("password",password)
        # print("passwords1",password1)
    
        # print("first name",first_name)
        # print("role",role)
        email = attrs.get('email')
        user=User.objects.filter(email=email)
        # if user.exists():
        #     if user.is_deleted==True:
        #         raise serializers.ValidationError("usealready exists")
        #     raise serializers.ValidationError("user with this email address already exists")

        if len(password)<6:
            raise serializers.ValidationError("Password length must be greater than six")
        if password != password1:
            raise serializers.ValidationError("Password doesn't match ")
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

class UserLoginSerilizer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    password=serializers.CharField(max_length=255)
    class Meta:
        model=User  
        fields=['email','password']

class UserPasswordChangeSerilizer(serializers.Serializer):
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Check your Password")
        user.set_password(password)
        user.save()
        return attrs
    
class EmailResetPasswordSerilizer(serializers.Serializer):
        email=serializers.EmailField(max_length=255)
        class Meta:
            fields=['email']
        def validate(self, attrs):
            email=attrs.get('email')
            if User.objects.filter(email=email).exists():
                user=User.objects.get(email=email)
                #create safe url 
                #convert user id to bytes
                uid=urlsafe_base64_encode(force_bytes(user.id))
                print(f'this is uid {uid}')
                
                token=PasswordResetTokenGenerator().make_token(user)
                print(f'this is token {token}')
                link='https://vmclub.a2zcyberpark.com/resetEpassword/'+uid+'/'+token
                print(link)
                body = 'Click on the link to reset your password: ' + link + '' 
                #send email
                data={
                    'subject':'Reset Your Password',
                    'body':body,
                    'to_email':user.email
                }
                Util.sendmail(data)
                
                return attrs
            else:
                raise ValueError("You are not a registered user")



class ResetPasswordSerilizer(serializers.Serializer):
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        try:
            if password != password2:
                raise serializers.ValidationError("changing Password doesn't match")
            #decoding and str ing uid
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('token is not valid or expired')




        

