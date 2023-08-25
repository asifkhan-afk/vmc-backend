from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serilizers import *
from django.contrib.auth import authenticate
# from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from datetime import datetime, timedelta
#creating token manually
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .utils import sendemail
from rest_framework_simplejwt.token_blacklist.models import  OutstandingToken,BlacklistedToken 

from doctor.models import DrProfile
from patient.models import PatientProfile
from student.models import StudentProfile
from hospital.models import HospitalProfile
# Create your views here.





class TokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


#generate token manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegestrationView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self,request):
        # print(request.data,'iiiiiiiiiiiii')
        data=request.data.copy()
        fname=data['first_name'].replace(" ", "")
        data['first_name']=fname
        print(data)
        
        serializer=UserRegSerilizer(data=data)
        email=request.data['email']
        print('this is emial of egistered user',email)
        try:
            usr=get_object_or_404(User.objects.all_objects(), email=email)
            if usr.is_deleted == True:
                 usr.delete()
                 print('usr is deleted')
        except:
            pass
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = get_tokens_for_user(user)
                try:
                    sendemail(user)
                    return Response({'token': token, 'msg': 'User has been created successfully'}, status=status.HTTP_201_CREATED)
                except:

                    return Response({'token': token, 'msg': 'User is not created'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except IntegrityError:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
       
        else:
            print("BBBBBBBBBBBBBB")
            errors = serializer.errors
            print(errors,'99999999999999')
            if 'email' in errors and 'user with this email address already exists' in errors['email']:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,userid):
        user = get_object_or_404(User.objects.all_objects(), id=userid)
        print(user,'this is user')
        if user:
            user.is_deleted=False
            user.save()
            instance=user
            if user.is_deleted:
                time_difference = datetime.now() - user.created_at
                if time_difference < timedelta(minutes=5):
                    user.delete()
                    return Response({'message':'activation link is expired','activated':'false'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if user.is_deleted==False:
             
             try:
                
                if instance.role == "doctor":
                    chek=DrProfile.objects.filter(name=instance)
                    if not chek:
                        dr=DrProfile.objects.create(name=instance)
                        dr.profemail=instance.email
                        
                        dr.save()
                elif instance.role == "patient":
                    chek=PatientProfile.objects.filter(name=instance)
                    if not chek:
                        pt=PatientProfile.objects.create(name=instance)
                        pt.profemail=instance.email
                        print("this is patient ,",pt)
                        
                        pt.save()
                elif instance.role == "student":
                    chek=StudentProfile.objects.filter(name=instance)
                    if not chek:
                        st=StudentProfile.objects.create(name=instance)
                        st.profemail=instance.email
                            
                        st.save()
                elif instance.role == "hospital":
                    chek=HospitalProfile.objects.filter(name=instance)
                    if not chek:
                        hs=HospitalProfile.objects.create(name=instance)
                        hs.email=instance.email
                        print("this is hospital profile ",hs)
                        
                        hs.save()
             except IntegrityError:
            # Handle the duplicate entry error
                pass



            return Response({'message':'user activated','activated':'true'},status=status.HTTP_201_CREATED)
        return Response({},status=status.HTTP_404_NOT_FOUND)
# class UserLoginView(APIView):
#     # renderer_classes=[UserRenderer]
#     def post(self,request):        
#         serilizer=UserLoginSerilizer(data=request.data)
#         if serilizer.is_valid(raise_exception=True):
#             email=serilizer.data.get('email')
#             password=serilizer.data.get('password')
#             print("EMAIL",email,"PASSWORD",password)
#             user=authenticate(email=email,password=password)           
#             if user is not None:
#                 # token=get_tokens_for_user(user)
#                 token="fumm yokm"
#                 # token=TokenView.as_view()
#                 return Response({'token':token,'msg':'login success'},status=status.HTTP_200_OK)
#             else:
#                 return Response({'errors':{'non_field_errors':['email or password is not correct hhh']}},status=status.HTTP_404_NOT_FOUND)

class UserLogOut(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
          print(request.META.get('Authorization'))
          try:
                refresh_token = request.data["refresh_token"]              
                token = RefreshToken(refresh_token)       
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               print("thi sis logout error",e)
               return Response(status=status.HTTP_400_BAD_REQUEST)
          

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class UserChangePassword(APIView):
    # renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserPasswordChangeSerilizer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password has been changed'},status=status.HTTP_200_OK)
        return Response({'msg':'password is not changed'},status=status.HTTP_400_BAD_REQUEST)


class EmailResetPasswordView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=EmailResetPasswordSerilizer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email=serializer.data['email']
            return Response({'msg':f'Password reset link has been send to {email}'},status=status.HTTP_200_OK)
        return Response({'msg':'you are not registered user'},status=status.HTTP_400_BAD_REQUEST)
        
class ResetPasswordView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        print("reset pass view")
        serializer=ResetPasswordSerilizer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password has been changed'},status=status.HTTP_200_OK)
        return Response({'msg':'password is not changed'},status=status.HTTP_400_BAD_REQUEST)
    

class Userlistview(APIView):
    def get(self,request,userid=None):
        if userid:
            user=User.objects.get(id=userid)
            serilizer=UserSerializer(user)
            print(serilizer.data,'pppp')
        else:
            user=User.objects.all()
            serilizer=UserSerializer(user,many=True)
        return Response(serilizer.data,status=status.HTTP_200_OK)

    


