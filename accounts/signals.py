from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User
from doctor.models import DrProfile
from patient.models import PatientProfile
from student.models import StudentProfile
from hospital.models import HospitalProfile
from appointment.models import Appointment

#Doctor
# @receiver(post_save, sender=User)






@receiver(post_save, sender=Appointment)
def sendemail(sender, instance, created, **kwargs):
    if created:
        if instance.doctor:
            dremail = instance.doctor.name.email
            send_email_to = [dremail]
        elif instance.hospital:
            hsemail = instance.hospital.name.email
            send_email_to = [hsemail]
        else:
            return  # No doctor or hospital present, do not send email
        
        ptemail = instance.patient.name.email
        print("sending appointment email", send_email_to, ptemail)
        subject = "Appointment"
        apptime=instance.scheduled_time
        appdate=instance.scheduled_date
        if instance.doctor:
            link = f"https://vmclub.a2zcyberpark.com/appointment/{instance.doctor.name.id}/appointmentlist"
        else:
            link = f"https://vmclub.a2zcyberpark.com/appointment/{instance.hospital.name.id}/appointmentlist"
        ptlink = f"https://vmclub.a2zcyberpark.com/appointment/{instance.patient.name.id}/ptappointmentlist"
        loginlink = "https://vmclub.a2zcyberpark.com/"

        # Email notification for the doctor or hospital
        if instance.doctor:
            html_message = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>New Appointment</title>
            </head>
            <body>
                <h1>New Appointment</h1>
                <p>Hi {doctor_first_name} {doctor_last_name},</p>
                <p>A new appointment has been scheduled on {appdate} at {apptime}  with {patient_first_name} {patient_last_name}.</p>
                <p>Click on the link below to view the appointment:</p>
                <a href="{link}">View Appointment</a>
                <p>If you are not logged in, click <a href="{loginlink}">here</a> to login.</p>
            </body>
            </html>
            """.format(doctor_first_name=instance.doctor.name.first_name,
                       doctor_last_name=instance.doctor.name.last_name,
                       patient_first_name=instance.patient.name.first_name,
                       patient_last_name=instance.patient.name.last_name,
                       link=link,
                       loginlink=loginlink,
                       appdate=appdate,
                       apptime=apptime
                       
                       )
        else:
            html_message = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>New Appointment</title>
            </head>
            <body>
                <h1>New Appointment</h1>
                <p>Hi {hospital_name}'s, admin</p>
                <p>Please check your account.  {patient_first_name} {patient_last_name} want to book an appointment on {appdate} at {apptime} .</p>
                <p>Click on the link below to view the appointment:</p>
                <a href="{link}">View Appointment</a>
                <p>If you are not logged in, click <a href="{loginlink}">here</a> to login.</p>
            </body>
            </html>
            """.format(hospital_name=instance.hospital.name,
                       patient_first_name=instance.patient.name.first_name,
                       patient_last_name=instance.patient.name.last_name,
                       link=link,
                       loginlink=loginlink,
                       appdate=appdate,
                       apptime=apptime


                       
                       )

        text_message = strip_tags(html_message)
        print("sending email")

        email = EmailMultiAlternatives(subject, text_message, settings.EMAIL_HOST_USER, send_email_to)
        email.attach_alternative(html_message, "text/html")
        email.send()
        print("email sent")

        # Email notification for the patient
        html_message_patient = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Appointment</title>
        </head>
        <body>
            <h1>Appointment Update</h1>
            <p>Hi {patient_first_name} {patient_last_name},</p>
            <p>Your appointment has been scheduled on {appdate} at {apptime}. Please visit on time</p>
            <p>Click on the link below to view the appointment:</p>
            <a href="{ptlink}">View Appointment</a>
            <p>If you are not logged in, click <a href="{loginlink}">here</a> to login.</p>
        </body>
        </html>
        """.format(patient_first_name=instance.patient.name.first_name,
                   patient_last_name=instance.patient.name.last_name,
                   ptlink=ptlink,
                   loginlink=loginlink,
                   appdate=appdate,
                   apptime=apptime
                       

                   
                   )
        print("patinet email")
                   

        text_message_patient = strip_tags(html_message_patient)

        email_patient = EmailMultiAlternatives(subject, text_message_patient, settings.EMAIL_HOST_USER, [instance.patient.name.email])
        email_patient.attach_alternative(html_message_patient, "text/html")
        print("sending patient email")
        email_patient.send()
        print("patinet email has been sended")


@receiver(post_save, sender=Appointment)
def sendupdateemail(sender, instance, created, **kwargs):
    if not created:
        subject = "Appointment Update"
        ptlink = f"https://vmclub.a2zcyberpark.com/appointment/{instance.patient.name.id}/ptappointmentlist"
        loginlink = "https://vmclub.a2zcyberpark.com/"
        # Email notification for the patient
        html_message_patient = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Appointment</title>
        </head>
        <body>
            <h1>Appointment Update</h1>
            <p>Hi {patient_first_name} {patient_last_name},</p>
            <p>Your appointment status has been updated.</p>
            <p>Click on the link below to view the appointment:</p>
            <a href="{ptlink}">View Appointment</a>
            <p>If you are not logged in, click <a href="{loginlink}">here</a> to login.</p>
        </body>
        </html>
        """.format(patient_first_name=instance.patient.name.first_name,
                   patient_last_name=instance.patient.name.last_name,
                   ptlink=ptlink,
                   loginlink=loginlink)
                   
                   
        print("patinet update")
        text_message_patient = strip_tags(html_message_patient)

        email_patient = EmailMultiAlternatives(subject, text_message_patient, settings.EMAIL_HOST_USER, [instance.patient.name.email])
        email_patient.attach_alternative(html_message_patient, "text/html")
        print("sendign patine tupdate")
        email_patient.send()
        print("patient update email has been sended")
        
        # Email notification for the doctor
        if instance.status== 'accepted':
            if instance.doctor:
                rec=instance.doctor.name.first_name
            else:
                rec=instance.doctor.name.first_name
            time=instance.scheduled_time
            html_message_doctor = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Appointment</title>
            </head>
            <body>
                <h1>Appointment</h1>
                <p>Hi {doctor_first_name} ,</p>
                
                <p>You have accepted the appointment request from {patient_first_name} {patient_last_name}.</p>
        <p>The appointment is scheduled at {apptime} on {appdate}.</p>
                <p>Click on the link below to view the appointment:</p>
                <a href="{link}">View Appointment</a>
                <p>If you are not logged in, click <a href="{loginlink}">here</a> to login.</p>
            </body>
            </html>
            """.format(doctor_first_name=rec,
                    #    doctor_last_name=instance.doctor.name.last_name,
                       patient_first_name=instance.patient.name.first_name,
                       patient_last_name=instance.patient.name.last_name,
                       link=link,
                       loginlink=loginlink,
                       apptime=instance.scheduled_time,
                       appdate=instance.scheduled_date
                       )
    
            text_message_doctor = strip_tags(html_message_doctor)
            print("sending update dr email")
    
            email_doctor = EmailMultiAlternatives(subject, text_message_doctor, settings.EMAIL_HOST_USER, [instance.doctor.name.email])
            print("3")
            email_doctor.attach_alternative(html_message_doctor, "text/html")
            print("before dr update send",email_doctor)
            email_doctor.send()
            print("after dr update send")