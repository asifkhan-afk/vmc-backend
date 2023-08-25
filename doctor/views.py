from django.shortcuts import get_object_or_404
from rest_framework .response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serilizers import *
from rest_framework import viewsets
# from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from django.db.models import Count
from social.models import Notification

# Assuming you have a Post model with a foreign key to User model
# users_with_post_count = User.objects.annotate(post_count=Count('post'))

# for user in users_with_post_count:
#     print(f"User: {user.username}, Post Count: {user.post_count}")

#creating token manually
# from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

# #generate token manually 
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
# Create your views here.


class WorkExperienceView(APIView):
    def get(self,request,drid=None,spid=None):
        user=request.user
        dr=get_object_or_404(DrProfile,name=drid)
        
        edu=WorkExperience.objects.filter(dr=dr)
        print(edu)
        serilizer=WorkxperienceSerilizer(edu,many=True)
        print(serilizer.data)
        return Response(serilizer.data)
    
    def post(self,request,drid=None,eduid=None):
        print(request.data)
        if drid:
            requser=get_object_or_404(User,id=drid)
            dr=get_object_or_404(DrProfile,name=requser)
        user=request.user
      
        if user==requser:
            edu=WorkExperience.objects.create(dr=dr,company=request.data['company'],position=request.data['position'],start_date=request.data['start_date'],end_date=request.data['end_date'],is_current=False)
            edu.save()
   
        return Response({'msg':'speciality created'})
    
    def delete(self,request,eduid=None,drid=None):
        user=request.user
        
        sp=get_object_or_404(WorkExperience,id=eduid)
        print(sp)
        if sp.dr.name==user:
            sp.delete()
            return Response({'msg':'deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response ({'msg':'fail to delte '})

    






class EducationView(APIView):
    def get(self,request,drid=None,spid=None):
        user=request.user
        dr=get_object_or_404(DrProfile,name=drid)
        
        edu=Education.objects.filter(dr=dr)
        print(edu)
        serilizer=EducationSerilizer(edu,many=True)
        print(serilizer.data)
        return Response(serilizer.data)
    
    def post(self,request,drid=None,eduid=None):
        print(request.data)
        if drid:
            requser=get_object_or_404(User,id=drid)
            dr=get_object_or_404(DrProfile,name=requser)
        user=request.user
      
        if user==requser:
            edu=Education.objects.create(dr=dr,degree=request.data['degree'],institute=request.data['institute'],start_date=request.data['start_date'],end_date=request.data['end_date'],is_graduated=False)
            edu.save()
   
        return Response({'msg':'speciality created'})
    
    def delete(self,request,eduid=None,drid=None):
        user=request.user
        
        sp=get_object_or_404(Education,id=eduid)
        print(sp)
        if sp.dr.name==user:
            sp.delete()
            return Response({'msg':'deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response ({'msg':'fail to delte '})

    
class DrSpecialityView(APIView):
    def get(self,request,drid=None,spid=None):
        user=request.user
        dr=get_object_or_404(DrProfile,name=drid)
        print(dr)
        sp=Speciality.objects.filter(dr=dr)
        print(sp)
        serilizer=GetSpecialitySerilizer(sp,many=True)
        print(serilizer.data)
        return Response(serilizer.data)
    
    def post(self,request,drid=None,spid=None):
        print(request.data)
        if drid:
            requser=get_object_or_404(User,id=drid)
            dr=get_object_or_404(DrProfile,name=requser)
        user=request.user
        print(user.first_name,'user')
        print(dr.name.first_name,'dr')
        if user==requser:
            s=Speciality.objects.create(dr=dr,name=request.data['name'])
            s.save()
            print("this iss s",s)

        print('no posting')
        return Response({'msg':'speciality created'})
    
    def delete(self,request,spid=None,drid=None):
        user=request.user
        print(user,spid)
        sp=get_object_or_404(Speciality,id=spid)
        print(sp)
        if sp.dr.name==user:
            sp.delete()
            return Response({'msg':'deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response ({'msg':'fail to delte '})
    # serializer_class=SpecialitySerilizer
    # queryset=Speciality.objects.all()


class DrProfileView(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request,pk=None):
        user=request.user.id
        if pk:
            dr=get_object_or_404(User,pk=pk).pk
            drp=DrProfile.objects.get(name=dr) 
            print('dddrrrrrrrrrrrrrrr')
            serilizer=DrProfileSerilizer(drp)   
        else:
            dr=DrProfile.objects.all()
            serilizer=DrProfileSerilizer(dr,many=True)
        return Response(serilizer.data)
    
    def put(self,request,pk=None):
        user=request.user
        userid=user.id
        if pk==userid:
            
            data=request.data
            print("this is formd data", data)
            if 'first_name' in data:
                user.first_name=data['first_name']
            if 'last_name' in data:
                user.last_name=data['last_name']
            if 'profemail' in data:
                user.email=data['profemail']
            if 'profilepic' in data:
                user.profilepic=data['profilepic']
                
            user.save()
            print(request.data['profemail'])
            dr=DrProfile.objects.get(name_id=pk)
            serilizer=DrProfileSerilizer(instance=dr, data=request.data, partial=True)
            if serilizer.is_valid(raise_exception=True):
               
                serilizer.save()
                return Response(serilizer.data,status=status.HTTP_200_OK)
            return Response({"msg":"Doctor serilizer data is invalid"},status=status.HTTP_304_NOT_MODIFIED)
        return Response({"msg":"doctor id is missing"},status=status.HTTP_304_NOT_MODIFIED)

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    # renderer_classes=[UserRenderer]
    # # permission_classes=[IsAuthenticated]
    # def get(self,request,pk=None):
    #     if pk:
    #         profiles = DrProfile.objects.get(pk=pk)
    #         serializer = DrProfileSerilizer(profiles)
    #     else:
    #         profiles = DrProfile.objects.all()
    #         serializer = DrProfileSerilizer(profiles, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = DrProfileSerilizer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, pk):
    #     profile = DrProfile.objects.get(pk=pk)
    #     print("this is profile put ", profile)
    #     serializer = DrProfileSerilizer(profile, data=request.data)
        
    #     if serializer.is_valid(raise_exception=True):
    #         print("this is valid serilized put profile", serializer)     
    #         serializer.save()       
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics

from django.db.models import Q

class DrProfileList(generics.ListAPIView):
    serializer_class = DrProfileSerilizer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')  # Get the search query from the query parameters
        queryset = DrProfile.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |  # Filter by name
                Q(specialities__name__icontains=search_query) |  # Filter by speciality name
                Q(address__icontains=search_query) |  # Filter by address
                Q(education__institute__icontains=search_query) |  # Filter by education institute
                Q(education__degree__icontains=search_query)  # Filter by education degree
            )

        return queryset


class ResearchView(APIView):
    def get(self,request,drid=None,resid=None):

        if resid:
            research=get_object_or_404(Research,id=resid)
            serilizer=ResearchSerilizer(research)
            return Response(serilizer.data)
        
        if drid:
            dr=get_object_or_404(DrProfile,name=drid)
            print("dr sabe",dr)
            research=Research.objects.filter(doctor=dr)
            if research:
                serilizer=ResearchSerilizer(research,many=True)
                return Response(serilizer.data)
        else:
            research=Research.objects.all()
            if research:
                serilizer=ResearchSerilizer(research,many=True)
                return Response(serilizer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, drid=None, resid=None):
        if drid:
            print("user", request.user)
            dr = DrProfile.objects.get(name_id=drid)
            print("docotr in research", dr)
            if request.user == dr.name:
                # print('usr', request.user, hs.name,request.data)
                request.data._mutable=True
                request.data['doctor']=dr.id
                request.data._mutable=False
                serializer = ResearchPostSerilizer(data=request.data)
                print("))))))))))))))",request.data,'data')
                followers=request.user.get_followers()
                followers_id=[]
                for i in followers:
                    if i.follower.role=='student':
                        followers_id.append(i.follower.id)
                if serializer.is_valid(raise_exception=True):
                    
                    serializer.save()
                    Notification.objects.create(user_id=request.user.id,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message=" Shared a new Research Vacancy ",url=f"research",receiver_id=followers_id)
           
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,resid=None):
        res=get_object_or_404(Research,id=resid)
        if res:
            if res.doctor.name==request.user:
                res.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                print("nottt")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            print("you are not the owner of reserach")
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,resid=None):
        res=get_object_or_404(Research,id=resid)
        if res:
            if res.doctor.name==request.user:
                
                serializer=ResearchPostSerilizer(instance=res, data=request.data,partial=True)
                if serializer.is_valid(raise_exception=True):
                    print("seri is valid . ")
                    serializer.save()
                    # print("udated",serializer.data[''])
                    # Notification.objects.create(user_id=request.user.id,name=request.user.first_name,message=" Shared a new Research Vacancy ",url=f"home/postdetail/{serializer.data['id']}",receiver_id=followers_id)
           
                
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            else:
                print("nottt")
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            print("you are not the owner of reserach to update")
            return Response(status=status.HTTP_404_NOT_FOUND)



class ResearchApplyView(APIView):
    def post(self,request,researchid=None):
        if researchid:
            # print(request.data)
            data = request.data.copy()
            res=get_object_or_404(Research,id=researchid)
            data['research'] = researchid
            user=request.user
            # print(user.id)
            st=get_object_or_404(StudentProfile,name=user)
            
            data['student']=st.id
            
            serializer = ResearchApplyPOSTSerializer(data=data)
            
            if serializer.is_valid(raise_exception=True):
                
                serializer.save()
                # print("print reaseac doctor ",serializer.data['research'])
                doctor=DrProfile.objects.get(research=serializer.data['research'])
                doc=get_object_or_404(User,drprofile=doctor).id
                
                Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message=" Applied for research vacancy",url=f"researchlist/{request.user.id}/res/{serializer.data['research']}",receiver_id=[doc])
               
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,researchid=None,studentid=None,resapplyid=None):
        # hs=get_object_or_404(HospitalProfile,name=request.user)
        if researchid:
            res=Research.objects.get(id=researchid)
            applies=ResearchApply.objects.filter(research=res)
            serilizer=ResearchApplySerializer(applies,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
        if studentid:
            user=get_object_or_404(User,id=studentid)
            st=get_object_or_404(StudentProfile,name=user)
            applies=ResearchApply.objects.filter(student=st)
            serializers=StudentResearchApplySerializer(applies, many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        if resapplyid:
            applys=ResearchApply.objects.get(id=resapplyid)
            serializers=StudentResearchApplySerializer(applys)
            return Response(serializers.data,status=status.HTTP_200_OK)
    
    def put(self,request,resapplyid=None):
        apply=get_object_or_404(ResearchApply,id=resapplyid)
        user=request.user
        if user==apply.research.doctor.name:
            # print(request.data['update'])
            print(apply.status)
            apply.status=request.data['update']
            apply.save()
            n_reciever=apply.student.name.id
            Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}'  ,message=" viewed your research application. Please visit the site to check your application status",url=f"studentresapplylist/{n_reciever}/researchdet/{apply.id}",receiver_id=[n_reciever])
        return Response({'message':'Reasearch apply status has been changed'},status=status.HTTP_200_OK)