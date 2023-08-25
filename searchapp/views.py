from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework .response import Response
from rest_framework import status
from django.db.models import Q
from doctor.models import DrProfile,Research
from doctor.serilizers import DrProfileSerilizer,ResearchSerilizer
from student.models import StudentProfile
from student.serilizers import StudentProfileSerilizer
from patient.models import PatientProfile
from patient.serilizers import PatientProfileSerilizer
from hospital.models import HospitalProfile,Job
from hospital.serilizers import HospitalGetProfileSerilizer,HospitalJobySerilizer



# Create your views here.






# class DrSearchView(APIView):
#     serializer_class = DrProfileSerilizer

#     def get(self, request, format=None):
#         print(self.request.query_params)
#         search_query = self.request.query_params.get('s', '')
#         print(search_query)
       
#         if search_query:
#             queryset = DrProfile.objects.filter(
#                Q(name__first_name__icontains=search_query) |
#                  Q(name__last_name__icontains=search_query) 
#                 # Q(specialities__name__icontains=search_query) |
#                 # Q(address__icontains=search_query) |
#                 # Q(education__institute__icontains=search_query) |
#                 # Q(education__degree__icontains=search_query)
#             )

#             if not queryset.exists():
#                 return Response({'message': 'No results found.'}, status=status.HTTP_404_NOT_FOUND)

#             serializer = self.serializer_class(queryset, many=True)
#             return Response(serializer.data)
        
#         return Response({'message': 'Please provide a search query.'}, status=status.HTTP_400_BAD_REQUEST)






# class StSearchView(APIView):
#     serializer_class = StudentProfileSerilizer

#     def get(self, request, format=None):
#         search_query = self.request.query_params.get('s', '')
      

#         if search_query:
#             queryset = StudentProfile.objects.filter(
#                  Q(name__first_name__icontains=search_query) |
#                  Q(name__last_name__icontains=search_query) |
#                 Q(education__institute__icontains=search_query) |
#                 Q(education__degree__icontains=search_query)
#             )

#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)







class DrSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            drs = DrProfile.objects.filter(Q(name__first_name__icontains=x) | Q(name__last_name__icontains=x))
            if drs:
                serializer=DrProfileSerilizer(drs,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)
    

class StSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            st = StudentProfile.objects.filter(Q(name__first_name__icontains=x) | Q(name__last_name__icontains=x))
            if st:
                serializer=StudentProfileSerilizer(st,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)
    
class PtSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            st = PatientProfile.objects.filter(Q(name__first_name__icontains=x) | Q(name__last_name__icontains=x))
            if st:
                serializer=PatientProfileSerilizer(st,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)
    

class HsSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            st = HospitalProfile.objects.filter(Q(name__first_name__icontains=x) | Q(name__last_name__icontains=x))
            if st:
                serializer=HospitalGetProfileSerilizer(st,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)
    

class ResearchSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            st = Research.objects.filter(Q(title__icontains=x) | Q(skills_required__icontains=x))
            if st:
                serializer=ResearchSerilizer(st,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)
    
class JobSearchView(APIView):
    def get(self,request):

        x = request.GET.get('s')
        if x is not None:      
            st = Job.objects.filter(Q(position__icontains=x) | Q(qualification__icontains=x)| Q(requirements__icontains=x))
            if st:
                serializer=HospitalJobySerilizer(st,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'No data founded'},status=status.HTTP_204_NO_CONTENT)