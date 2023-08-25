from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework .response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serilizers import *
from rest_framework import viewsets
from django.contrib.auth import authenticate
# from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
#creating token manually
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser,FormParser





class WorkExperienceView(APIView):
    def get(self,request,stid=None,spid=None):
        user=request.user
        st=get_object_or_404(StudentProfile,name=stid)
        
        edu=WorkExperience.objects.filter(st=st)
        print(edu)
        serilizer=WorkxperienceSerilizer(edu,many=True)
        print(serilizer.data)
        return Response(serilizer.data)
    
    def post(self,request,stid=None,eduid=None):
        print(request.data)
        if stid:
            requser=get_object_or_404(User,id=stid)
            st=get_object_or_404(StudentProfile,name=requser)
        user=request.user
      
        if user==requser:
            edu=WorkExperience.objects.create(st=st,company=request.data['company'],position=request.data['position'],start_date=request.data['start_date'],end_date=request.data['end_date'],is_current=False)
            edu.save()
   
        return Response({'msg':'speciality created'})
    
    def delete(self,request,eduid=None,stid=None):
        user=request.user
        
        exp=get_object_or_404(WorkExperience,id=eduid)
       
        if exp.st.name==user:
            exp.delete()
            return Response({'msg':'deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response ({'msg':'fail to delte '})

    



class EducationView(APIView):
    def get(self,request,stid=None):
        user=request.user
        st=get_object_or_404(StudentProfile,name=stid)
        
        edu=Education.objects.filter(st=st)
        print(edu)
        serilizer=EducationSerilizer(edu,many=True)
        print(serilizer.data)
        return Response(serilizer.data)
    
    def post(self,request,stid=None,eduid=None):
        print(request.data)
        if stid:
            requser=get_object_or_404(User,id=stid)
            dr=get_object_or_404(StudentProfile,name=requser)
        user=request.user
      
        if user==requser:
            edu=Education.objects.create(st=dr,degree=request.data['degree'],institute=request.data['institute'],start_date=request.data['start_date'],end_date=request.data['end_date'])
            edu.save()
   
        return Response({'msg':'speciality created'})
    
    def delete(self,request,eduid=None,stid=None):
        user=request.user
        
        sp=get_object_or_404(Education,id=eduid)
        print(sp)
        if sp.dr.name==user:
            sp.delete()
            return Response({'msg':'deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response ({'msg':'fail to delte '})

    




class StudentProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request,pk=None):
        if pk:
            user=get_object_or_404(User,id=pk)
            st=StudentProfile.objects.get(name=user)
            serilizer=StudentProfileSerilizer(st)
        else:
            st=StudentProfile.objects.all()
            serilizer=StudentProfileSerilizer(st,many=True)
        return Response(serilizer.data)
    
    def put(self,request,pk=None):
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDD")
        user=request.user
        userid=user.id
        if pk==userid:
            
            data=request.data
            # print("this is formd data", data)
            if 'first_name' in data:
                user.first_name=data['first_name']
            if 'last_name' in data:
                user.last_name=data['last_name']
            if 'profemail' in data:
                user.email=data['profemail']
            if 'profilepic' in data:
                user.profilepic=data['profilepic']
                
            user.save()
        if pk:
            user=get_object_or_404(User,id=pk)
            st=StudentProfile.objects.get(name=user)
            serilizer=StudentProfileSerilizer(instance=st, data=request.data,partial=True)
            if serilizer.is_valid(raise_exception=True):
                serilizer.save()
                return Response(serilizer.data,status=status.HTTP_200_OK)
            print(serilizer.errors)
            return Response({"msg":"student serilizer data is invalid"},status=status.HTTP_304_NOT_MODIFIED)
          
        return Response({"msg":"id is missing"},status=status.HTTP_304_NOT_MODIFIED)