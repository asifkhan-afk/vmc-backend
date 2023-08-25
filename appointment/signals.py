# from django.conf import settings
# from django.db.models.signals import post_save
# from .models import Appointment
# from django.dispatch import receiver
# from django.core.mail import send_mail




# # from django.core.mail import EmailMultiAlternatives
# # from django.template.loader import render_to_string
# # from django.utils.html import strip_tags

# # def send_email():
# #     subject = 'Welcome to my website'
# #     from_email = 'asifkhan15848@gmail.com'
# #     to_email = 'asifkhan15848@gmail.com'
    
# #     # Plain text version of email
# #     text_content = 'Thanks for signing up!'
    
# #     # HTML version of email
# #     html_content = render_to_string('email_template.html', {'name': 'John Doe'})
    
# #     # Strip HTML tags for plain text version
# #     text_content = strip_tags(html_content)
    
# #     # Create email message with both plain text and HTML versions
# #     message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=[to_email])
# #     message.attach_alternative(html_content, 'text/html')
# #     message.body = text_content
    
# #     # Send email
# #     message.send()


# @receiver(post_save, sender=Appointment)
# def sendmail(sender, instance, created, **kwargs):
#     if created:
#         patient=instance.patient
#         print('patient email',patient)
#         dr=instance.doctor.email
#         print('patient email',dr)
#         scheduled_time=instance.scheduled_time
#         duration=instance.duration
#         send_mail(f'New Appointment Request from {patient.first_name}  at {scheduled_time} for {duration} minutes','this is tesjflks  ad fj flksjad flsdfj lkasjf saldfj alsdflask f sljf lasdfls asf jdlf alfls f adsf lsf as dfas jdlst mail',settings.EMAIL_HOST_USER,['asifkhan15848@gmail.com'])
       




            