from django.core.mail import EmailMessage
import os
#mobile number
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.utils.html import strip_tags
# import random
# def generate_random_numbers():
#   numbers = []
#   for i in range(6):
#     numbers.append(random.randint(1, 9))
  
#   return numbers

def sendemail(user):
    
        subject = "Account Activation"
        actlink = f"https://vmclub.a2zcyberpark.com/accountactivation/{user.id}"
        
       
        html_message = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Account Activation</title>
        </head>
        <body>
            <h1>Click to activate</h1>
            <h5>Dear {user_first_name} {user_last_name}</h5>
            
            <p>Thank you for registering on our platform! Please click on the link below to activate your account:</p>
            <a href="{actlink}">Activate</a>
            
        </body>
        </html>
        """.format(user_first_name=user.first_name,
                   user_last_name=user.last_name,
                   actlink=actlink)
                   
                   
        print("patinet update")
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(subject, text_message, settings.EMAIL_HOST_USER, [user.email])
        email.attach_alternative(html_message, "text/html")
        print("sending activation email")
        email.send()
        print(" account activation email has been sended")
        
        







class Util:
    @staticmethod
    def sendmail(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data['to_email']]
        )
        email.send()


#Mobile number
class MobileNumberField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r'^\+?\d{9,15}$',
            message='Mobile number must be in international format, e.g. +1234567890'
        )
    ]
    description = "Mobile number in international format, e.g. +1234567890"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)