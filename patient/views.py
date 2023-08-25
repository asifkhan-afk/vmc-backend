from rest_framework .response import Response
from rest_framework import status
from rest_framework.views import APIView
import re
from doctor.models import DrProfile,Speciality
from doctor.serilizers import DrProfileSerilizer
from .serilizers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser,FormParser
# import openai



class PatientProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request,pk=None):
        user=request.user.id
        if pk:
            pt=get_object_or_404(User,pk=pk).pk
            drp=PatientProfile.objects.get(name=pt) 
                 
            serilizer=PatientProfileSerilizer(drp)   
        else:
            pt=PatientProfile.objects.all()
            print("getting all pt prof")     

            serilizer=PatientProfileSerilizer(pt,many=True)
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
            pt=PatientProfile.objects.get(name_id=pk)
            serilizer=PatientProfileSerilizer(instance=pt, data=request.data, partial=True)
            if serilizer.is_valid(raise_exception=True):
               
                serilizer.save()
                return Response(serilizer.data,status=status.HTTP_200_OK)
            return Response({"msg":"Doctor serilizer data is invalid"},status=status.HTTP_304_NOT_MODIFIED)
        return Response({"msg":"doctor id is missing"},status=status.HTTP_304_NOT_MODIFIED)

# a=

# class AIQuestionareView(APIView):
    
    
#     def post(self,request):
        
#         symptoms=request.data['symptoms']
#         print(symptoms)
#         if symptoms:
            
#             api_key='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'
#             openai.api_key=api_key
            
#             question=f"i am having {symptoms}"

#             if api_key:
#                 prompt=f"{question}' if the question is only symptoms . anser only the speciality name who can cure that disease. other wise anser 'irrevelant entry'"
#                 response= openai.Completion.create(model="text-davinci-003", prompt=prompt,
#                                                    temperature=0.3,
#                                                    max_tokens=256)
#                 response=response.choices[0].text
#                 specialty_pattern = re.compile(r'\b(?:Cardiologist|Pulmonologist|Gastroenterologist|Nephrologist|Neurologist|Rheumatologist|Dermatologist|Urologist|Endocrinologist|OB-GYN|Ophthalmologist|ENT|Psychiatrist|Immunologist|Hematologist)\b')
#                 specialty = specialty_pattern.search(response)

              
#                 specialty=specialty.group(0)
           
#                 if response:
          
#                     drs = DrProfile.objects.filter(specialities__name__icontains=specialty)
                    
#                     if drs:
                        
#                         serializer=DrProfileSerilizer(drs,many=True)
                        
#                         data={'doctors':serializer.data,'data':response}
#                         return Response({'data':data},status=status.HTTP_200_OK)
                    
#                     data={'doctors':'','data':response}
#                     return Response({'data':data},status=status.HTTP_200_OK)
                
#                 data={'data':response}
#                 return Response(data,status=status.HTTP_200_OK)
            
#             return Response({'data':'AI model is busy Please try later'},status=status.HTTP_204_NO_CONTENT)
#         else:
#             print("no syptoms for ai")
#             return Response({'data':'You didnt selct any symptoms'},status=status.HTTP_204_NO_CONTENT)

           



class QuestionareView(APIView):
    
    def post(self, request):
        symptoms = request.POST.getlist('symptoms[]')

        if not symptoms:
            return Response({'data': 'You didnt select any symptoms'}, status=status.HTTP_204_NO_CONTENT)

        specialist_mapping = {
  'Chest pain or discomfort': 'Cardiologist',
  'Prolonged cough': 'Pulmonologist',
  'Nausea or vomiting': 'Gastroenterologist',
  'Blood in your urine': 'Nephrologist',
  'Numbness or tingling': 'Neurologist',
  'Joint pain or swelling': 'Rheumatologist',
  'A rash or itchy skin': 'Dermatologist',
  'Urinating more frequently': 'Urologist',
  'Excessive fatigue or weakness': 'Endocrinologist',
  'Recent unexplained weight loss': 'Endocrinologist',
  'Heavy menstrual bleeding': 'OB-GYN',
  'Blurry vision or vision changes': 'Ophthalmologist',
  'Hearing loss or ringing in ears': 'ENT',
  'Chronic headaches': 'Neurologist',
  'Blood in your stool': 'Gastroenterologist',
  'Depression or anxiety': 'Psychiatrist',
  'Swollen glands or frequent infections': 'Immunologist',
  'Bruise or bleed easily': 'Hematologist',
  'Abdominal pain or bloating': 'Gastroenterologist',
  'Excessive thirst or frequent urination': 'Endocrinologist',
}

        
        for symptom in symptoms:
            specialist = specialist_mapping.get(symptom)
            if specialist:
                print("specialist",specialist)
                dr = DrProfile.objects.filter(specialities__name__icontains=specialist)
                dr=list(dr)
                doctor_ids = set()
                drs=[]

                for d in dr:
                   
                    if d.id not in doctor_ids:
                        drs.append(d)
                        doctor_ids.add(d.id)
                
        if drs:
         
                serializer=DrProfileSerilizer(drs,many=True)
                
                data=serializer.data
                return Response({'data':data},status=status.HTTP_200_OK)
        return Response({'msg':'No serach text founded'},status=status.HTTP_204_NO_CONTENT)


            # return Response({'data': ', '.join(specialists)}, status=status.HTTP_200_OK)
