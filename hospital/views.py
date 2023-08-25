from django.shortcuts import render,get_object_or_404
from rest_framework .response import Response
from rest_framework import status,generics
from rest_framework.views import APIView

from .serilizers import *
from rest_framework import viewsets
from django.contrib.auth import authenticate
# from accounts.renderers import UserRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from social.models import Notification
# from django.conf import settings
# from django.core.mail import send_mail
#creating token manually
# from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class HospitalProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request,pk=None):
        #print("about to send test email to me ")
        user=request.user.id
        # #print("about to send test email to me ")
        # send_mail('there is a new vaancy','this is tesjflks  ad fj flksjad flsdfj lkasjf saldfj alsdflask f sljf lasdfls asf jdlf alfls f adsf lsf as dfas jdlst mail',settings.EMAIL_HOST_USER,['ak9360575@gmail.com'])
        if pk:
            hs=get_object_or_404(User,pk=pk).pk
            hsp=HospitalProfile.objects.get(name=user)  
           
           
            serilizer=HospitalProfileSerilizer(hsp)  
           
        else:
            hs=HospitalProfile.objects.all()
            #print("about to send test email to me ")
            serilizer=HospitalProfileSerilizer(hs,many=True)
        #print('this si profile ',serilizer.data)
        return Response(serilizer.data)
    def put(self,request,pk=None):
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
                # print(data['profemail'],'pppppppppppppppppppppppppppppppp')
            if 'profilepic' in data:
                user.profilepic=data['profilepic']
            print(user)
            user.save()
                        
            hs=HospitalProfile.objects.get(name_id=pk)
            serilizer=HospitalProfileSerilizer(instance=hs, data=request.data, partial=True)
           
            if serilizer.is_valid(raise_exception=True):
                #print("cal valid")
                
                serilizer.save()
                return Response(serilizer.data,status=status.HTTP_200_OK)
            return Response({"msg":"hospital serilizer data is invalid"},status=status.HTTP_304_NOT_MODIFIED)
        return Response({"msg":"hospital id is missing"},status=status.HTTP_304_NOT_MODIFIED)



class GetHospitalProfileView(APIView):
    
    # parser_classes = (MultiPartParser, FormParser)
    def get(self,request,pk=None):
        # user=request.user.id
        # #print("hospital get view without auth")
        # send_mail('there is a new vaancy','this is tesjflks  ad fj flksjad flsdfj lkasjf saldfj alsdflask f sljf lasdfls asf jdlf alfls f adsf lsf as dfas jdlst mail',settings.EMAIL_HOST_USER,['ak9360575@gmail.com'])
        if pk:
            hs=get_object_or_404(User,pk=pk).pk
            hsp=HospitalProfile.objects.get(name=hs)  
            #print("with out auth")
           
           
            serilizer=HospitalProfileSerilizer(hsp)  
           
        else:
            hs=HospitalProfile.objects.all()
            #print("with out aut all")

            serilizer=HospitalProfileSerilizer(hs,many=True)
        return Response(serilizer.data)

class ApplyView(APIView):
    def post(self,request,jobid=None):
        if jobid:
            # #print(request.data)
            data = request.data.copy()
            job=get_object_or_404(Job,id=jobid)
            data['job'] = jobid
            user=request.user
            
            if user.role=='doctor':
                dr=get_object_or_404(DrProfile,name=user)
                data['doctor']=dr.id
                #print(dr,"this si sdoe")
            elif user.role =='student':
                st=get_object_or_404(StudentProfile,name=user)
                data['student']=st.id
                
            # if data['student'] and data['doctor']:
            #     #print("there is error in ur method to apply")
            #     return Response( status=status.HTTP_400_BAD_REQUEST)         
            # #print(data)
            # apply=Apply.objects.create(**request.data)joblist/4/jobdetapplylist/32
            #print('this i s data',data)
            serializer = ApplyPostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                
                Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}'  ,message="applied for Job Vacancy",url=f"joblist/{job.hospital.name.id}/jobdetapplylist/{jobid}",receiver_id=job.hospital.name.id)
       
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,jobid=None,applyid=None):
        # hs=get_object_or_404(HospitalProfile,name=request.user)
        if applyid:
            app=Apply.objects.get(id=applyid)
            serilizer=ApplySerializer(app)
      
            return Response(serilizer.data,status=status.HTTP_200_OK)
        job=Job.objects.get(id=jobid)
        applies=Apply.objects.filter(job=job)
        serilizer=ApplySerializer(applies,many=True)
        # #print(applies)
        # #print(serilizer)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,applyid=None):
        apply=get_object_or_404(Apply,id=applyid)
        n_reciever=None
        st=None
        dr=None
        #print(apply,'ppppppppppppppppppppppp')
        if apply.student:
            n_reciever=apply.student.name.id
            st=apply.student
        if apply.doctor:
            n_reciever=apply.doctor.name.id
            dr=apply.doctor
        user=request.user
        if user==apply.job.hospital.name:
            # #print(request.data['update'])
            #print(apply.status)
            apply.status=request.data['update']
            apply.save()
            #print("this si apply status",apply.status)
            Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}'  ,message="Viewed your Job application,",url=f"alljoblist/jobapplydetail/{applyid}",receiver_id=[n_reciever])
            if apply.status=='approved':
                Affiliated_doctors.objects.get_or_create(doctor=dr,student=st,hospital=apply.job.hospital,position=apply.job.position,confirmed=True)
            if apply.status=='rejected':
               
                afd=Affiliated_doctors.objects.filter(Q(position=apply.job.position) and Q(hospital=apply.job.hospital) and Q(student=st) and Q(doctor=dr))
                ##print(afd)
                afd.delete()
                

        return Response(status=status.HTTP_200_OK)


class GalleryApiView(APIView):
    
    # parser_classes = (MultiPartParser, FormParser)
    def get(self, request,hsid=None,id=None):
        if id:
            dpt=get_object_or_404(Gallery,id=id)
            serializer = GallerySerializer(dpt)
            
        else:
            

            dpt = Gallery.objects.filter(hospital=hsid)
            serializer = GallerySerializer(dpt, many=True)
           
        return Response(serializer.data)
    def post(self, request,hsid=None,):
        user=request.user.id
        #print('this is user',user)
        hsp=get_object_or_404(HospitalProfile,name=user)
        #print('this is hsp',hsp)
        
        data=request.data
        
        #print(data)
        gallery=Gallery.objects.create(caption=data['caption'],image=data['image'],hospital=hsp)
        gallery.save() 
        return Response( status=status.HTTP_201_CREATED)
        

        
    def put(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(Gallery, id=id)
        hsid=dpt.hospital.name
        #print('88888888888888888888888888888888888888888',request.data)
        if user==hsid:
            serializer = GallerySerializer(dpt, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                #print(serializer.data,'this is serilizer data')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(Gallery, id=id)
        hsid=dpt.hospital.name
        if user==hsid:
            
            dpt.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



    def perform_create(self, serializer):
        serializer.save(hospital=self.request.user.hospital_profile)
        





class HospitalVacancyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HospitalJobySerilizer

    def get_queryset(self):
        return Job.objects.all()


class HospitalDepartmentView(APIView):
    
    # parser_classes = (MultiPartParser, FormParser)
    def get(self, request,hsid=None,id=None):
        if id:
            dpt=get_object_or_404(HospitalDepartment,id=id)
            serializer = HospitalDepSerilizer(dpt)
        else:
            

            dpt = HospitalDepartment.objects.filter(hospital=hsid)
            serializer = HospitalDepartmentSerilizer(dpt, many=True)
        return Response(serializer.data)

    def post(self, request,hsid=None,):
        user=request.user.id
        #print('this is user',user)
        hsp=get_object_or_404(HospitalProfile,name=user)
        #print('this is hsp',hsp)
        
        data=request.data
        
        #print(data)
        hsdp=HospitalDepartment.objects.create(name=data['name'],dptphoto=data['dptphoto'],hospital=hsp,description=data['description'])
        # serializer = HospitalDepartmentSerilizer(data=request.data)
        hsdp.save()
        # #print('checking validinty')
        # if serializer.is_valid():
        #     #print('saving serilizer data')
        #     serializer.save()
        return Response( status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(HospitalDepartment, id=id)
        hsid=dpt.hospital.name
        #print('88888888888888888888888888888888888888888',request.data)
        if user==hsid:
            serializer = HospitalDepartmentSerilizer(dpt, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                #print(serializer.data,'this is serilizer data')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(HospitalDepartment, id=id)
        hsid=dpt.hospital.name
        if user==hsid:
            #print('deleted')
            dpt.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




class HospitalServicesView(APIView):
    
    # parser_classes = (MultiPartParser, FormParser)
    def get(self, request,hsid=None,id=None):
        #print("))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))")
        if id:
            dpt=get_object_or_404(HospitalServices,id=id)
            serializer = HospitalSerSerilizer(dpt)
        else:
            

            dpt = HospitalServices.objects.filter(hospital=hsid)
            serializer = HospitalServicesSerilizer(dpt, many=True)
        return Response(serializer.data)

    def post(self, request,hsid=None,):
        user=request.user.id
        #print('this is user',user)
        hsp=get_object_or_404(HospitalProfile,name=user)
        #print('this is hsp',hsp)
        
        data=request.data
        
        srphoto = data.get('srphoto', None) 
           
        #print(srphoto,'srphottttttt')
        
        #print(data)
        hsdp=HospitalServices.objects.create(name=data['name'],srphoto=srphoto,hospital=hsp,description=data['description'])
        #print(hsdp)
        hsdp.save()
     
        return Response( status=status.HTTP_201_CREATED)
       

    
    def put(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(HospitalServices, id=id)
        hsid=dpt.hospital.name
       
        if user==hsid:
            serializer = HospitalServicesSerilizer(dpt, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                #print(serializer.data,'this is serilizer data')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id=None):
        user=request.user
        dpt = get_object_or_404(HospitalServices, id=id)
        hsid=dpt.hospital.name
        if user==hsid:
            #print('deleted')
            dpt.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


class AffiliatedDoctorsView(APIView):
    def get(self,request,afdid=None,hsid=None):
        if afdid:
            afd=get_object_or_404(Affiliated_doctors,id=afdid)
            serializer = Affiliated_doctors_serilizer(afd)
        if hsid:
            hsuser=get_object_or_404(User,id=hsid)
            hs=get_object_or_404(HospitalProfile,name=hsuser).id
            afd=Affiliated_doctors.objects.filter(hospital__id=hs)
            if request.user.role !='hospital':
                afd=afd.filter(confirmed=True)
            serializer = Afdoctors_serilizer(afd, many=True)
        return Response(serializer.data)
    def put(self,request,afdid=None):
        if afdid:
            afd=get_object_or_404(Affiliated_doctors,id=afdid)
            # serializer = Affiliated_doctors_serilizer(afd,data=request.data ,partial=True)
            afd.delete()
            # if serializer.is_valid():
            #     serializer.save()
            return Response({},status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


    
    def post(self,request,hsid=None):
        user=request.user
        #print(user)
        dr=get_object_or_404(DrProfile,name=user)
        #print(dr)
        if hsid:
            hsuser=get_object_or_404(User,id=hsid)
            hs=get_object_or_404(HospitalProfile,name=hsuser)
            afd = Affiliated_doctors.objects.get_or_create(doctor=dr,hospital=hs,confirmed=False)
            #print("#printinf afd",afd)
            afd.save()
            return Response({'msg':'you request has been sended'},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    
class DrCreationView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        user=request.user.role
        if user=='doctor':
            serilizer=DrCreationSerilizer(data=request.data)
            if serilizer.is_valid(raise_exception=True):
                user=serilizer.save()
                
                
                return Response({'token':'token','msg':'user has been created successfully'},status=status.HTTP_201_CREATED)
        return Response({'msg':"errer in creating doctor"},status=status.HTTP_400_BAD_REQUEST)
    


class JobListView(APIView):
    def get(self,request):
            job=Job.objects.all()
            serilizer=HospitalJobySerilizer(job,many=True)
            return Response(serilizer.data)

class HospitalJobView(APIView):
    def get(self,request,hsid=None,jobid=None):
        if jobid:
            job=get_object_or_404(Job,id=jobid)
            serilizer=HospitalJobySerilizer(job)
            return Response(serilizer.data)
        
        hs=get_object_or_404(HospitalProfile,name_id=hsid)
        jobs=Job.objects.filter(hospital=hs)
        #print(hsid,HospitalProfile.objects.get(name=hsid))
        
        
        if jobs:
            serilizer=HospitalJobySerilizer(jobs,many=True)
            return Response(serilizer.data)
        return Response(status=status.HTTP_200_OK)
    
    def put(self,request,jobid=None):
        job=get_object_or_404(Job,id=jobid)
        
        serilizer=HospitalJobySerilizer(instance=job,data=request.data,partial=True)
        if serilizer.is_valid():
           
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
        
    def post(self, request, hsid=None, jobid=None):
        if hsid:
            #print("user", request.user)
            hs = HospitalProfile.objects.get(name_id=hsid)
            #print("hs", hs)
            if request.user == hs.name:
                # #print('usr', request.user, hs.name,request.data)
                request.data._mutable=True
                request.data['hospital']=hs.id
                request.data._mutable=False
                serializer = HospitalPostJobySerilizer(data=request.data)
                # #print("))))))))))))))",request.data,'data')
                followers=request.user.get_followers()
                followers_id=[]
                for i in followers:
                    if i.follower.role=='student' or i.follower.role =='doctor':
                        # #print(i.follower.role,'9999999999999999999999999999999999999999999999999999999999')
                        followers_id.append(i.follower.id)
                
                if serializer.is_valid(raise_exception=True):
                    # #print('sari is vaid')
                    serializer.save()
                    #print('saved')
                    Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}'  ,message="Shared a New Job Vacancy",url=f"alljoblist/{request.user.id}/jobdetail/{serializer.data['id']}",receiver_id=followers_id)
       
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self,request,jobid=None):
        job=get_object_or_404(Job,id=jobid)

        if request.user.id== job.hospital.name_id:

            if job:
                    #print('job to be deleted',job)
                    job.delete()
                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
                

from rest_framework import generics

class HsProfileList(generics.ListAPIView):
    serializer_class = HospitalProfileSerilizer

    def get_queryset(self):
       
        name = self.request.query_params.get('name', '')  # Get the name from the query parameters
        queryset = HospitalProfile.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)  # Perform case-insensitive filtering by name

        return queryset