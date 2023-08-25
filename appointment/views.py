from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.db.models import Q
from hospital.models import HospitalProfile
from .models import Appointment
from .serilizers import *
from django.shortcuts import get_object_or_404
from patient.views import PatientProfile
from doctor.views import DrProfile
from accounts.models import User
from django.core.mail import send_mail
from social.models import Notification
# Create your views here.


def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

class Availableslots(APIView):
    def post(self,request,drid):
            druser=get_object_or_404(User,id=drid)
            doctor=get_object_or_none(DrProfile,name=druser)
            date=request.data['date']
            # appointments = Appointment.objects.filter(doctor=doctor, scheduled_date=date)
            
            start_time = doctor.working_hours_start
            end_time = doctor.working_hours_end

            du = doctor.max_appointment_time
            dat=request.data['date']
            date = datetime.datetime.strptime(dat, '%Y-%m-%d').date()
            duration = datetime.timedelta(du)
           # Convert string to date object
            start_datetime = datetime.datetime.combine(date, start_time)
            end_datetime = datetime.datetime.combine(date, end_time)
            

            available_slots = []
            
            while start_datetime < end_datetime :
                print(start_datetime,'ssssssssssss')
                print(end_datetime,'ooooooooo')
                print(dat)
                
                appointment = Appointment.objects.filter(Q(scheduled_time__range=(start_time, end_time)) and Q(scheduled_date=(dat)))
                print(appointment.count())
                if appointment.count()>0:
                    for i in appointment:
                        starttime=start_datetime.time()
                        end=start_datetime+datetime.timedelta(minutes=du)
                        endtime=end.time()
                        
                        print(i.scheduled_time)
                        if i.scheduled_time==starttime:
                            start_datetime=end
                        else:
                            if start_datetime< end_datetime:
                                slot = f"{starttime}-{endtime}"
                                available_slots.append(slot)
                                start_datetime=end
                else:
                    # end=start_datetime+datetime.timedelta(minutes=du)
                    # start_datetime=end
                
                    starttime=start_datetime.time()
                    end=start_datetime+datetime.timedelta(minutes=du)
                    endtime=end.time()
                    slot = f"{starttime}-{endtime}"
                    available_slots.append(slot)
                    start_datetime=end
               
            return JsonResponse({"available_slots": available_slots})

class AppointmentView(APIView):
    model=Appointment
    def get(self,request,drid=None,ptid=None,appid=None):

        # today = datetime.date.today()
        if drid:
            druser=get_object_or_404(User,id=drid)
            dr=get_object_or_none(DrProfile,name=druser)
            if dr:
                apoint= Appointment.objects.filter(doctor=dr)
                # for i in apoint:
                #     print(i.scheduled_date)
                #     if i.scheduled_date < today:
                #        print("data")
                #        if i.status=='scheduled':
                #         i.status='completed'
                #         i.save()
                #         print(i)
               
                        
                
            else:
                hs=get_object_or_none(HospitalProfile,name=druser)
                
                
                apoint=Appointment.objects.filter(hospital=hs)
            
            serilizer=AppointmentSerilizer(apoint,many=True)
            
            return Response(serilizer.data)
        if ptid:
            ptuser=get_object_or_404(User,id=ptid)
            print(ptuser)
            pt=get_object_or_404(PatientProfile,name=ptuser)
            print(pt)
            apoint= Appointment.objects.filter(patient=pt)
            print(apoint)
            serilizer=AppointmentGetSerilizer(apoint,many=True)
            return Response(serilizer.data)
        if appid:
             
            # user=request.user
            # dr=get_object_or_none(DrProfile,name=user)
            # hs=get_object_or_none(HospitalProfile,name=user)
            print("getting single appontment 1")
            apoint=get_object_or_none(Appointment,id=appid)
            print("getting single appontment 2",apoint)
            serilizer=AppointmentGetSerilizer(apoint)
            return Response(serilizer.data)
        return Response({'msg':'doctor id not found'},status=status.HTTP_404_NOT_FOUND)
    

    def post(self,request,drid=None):
        user=request.user.id
        pt=get_object_or_404(PatientProfile,name=user)
        data=request.data.copy()
        
        if pt:
            print('this is pt',pt)
            druser=get_object_or_404(User,id=drid)
            
            dr=get_object_or_none(DrProfile,name=druser)
            print('thsds')
            n_reciever=[]
            if dr:
                data=request.data.copy()
                data['doctor'] = dr.id
                data['status'] ='scheduled'   
            else:
                hs=get_object_or_404(HospitalProfile,name=druser)
                data['hospital'] = hs.id
                

            
            n_reciever.append(druser.id)
            data['patient'] = pt.id   
                    
            serilizer=AppointmentSerilizer(data=data,partial=True)
            if serilizer.is_valid(raise_exception=True):
                serilizer.save()
                print("creating notification",n_reciever)
                Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message=" send you a new appointment request",url=f"appointment/:id/ptappointmentlist/appointmentdetail/{serilizer.data['id']}",receiver_id=n_reciever)
                print("created noti ")
                    
                return Response({'msg':'appointment created'},status=status.HTTP_201_CREATED)
            return Response({'msg':'seri is not valid '},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Only patinets can book appointment'},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,appid=None):
        user=request.user
        dr=get_object_or_none(DrProfile,name=user)
        hs=get_object_or_none(HospitalProfile,name=user)
        app=get_object_or_none(Appointment,id=appid)
        
        if app.doctor==dr or app.hospital==hs:
         
            print(request.data)
            serilizer=AppointmentSerilizer(app,data=request.data,partial=True)
            if serilizer.is_valid():
                serilizer.save()
                print("print patint e 999999999999999999999",app.patient.name.id)
                
                Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message="Has seen Your Request! See your appoint status",url=f"appointment/{request.user.id}/ptappointmentlist/appointmentdetail/{serilizer.data['id']}",receiver_id=[app.patient.name.id])
                return Response({},status=status.HTTP_200_OK)
            return Response({'msg':'No doctor or hospital is found'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'No doctor or hs is found'},status=status.HTTP_400_BAD_REQUEST)