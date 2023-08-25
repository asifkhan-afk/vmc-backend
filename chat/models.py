from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime
from django.utils.timezone import now
# Create your models here.
class Chat(models.Model):
   last_message_id=models.CharField(max_length=255)
   last_message_created_date=models.DateTimeField(auto_now=True)
   total_messages=models.CharField(max_length=255,default=0)
   sender_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_sender")
   reciever_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_reciever")
   created_at = models.DateTimeField(auto_now=True)
   updated_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering=['-updated_at']

MESSAGE_ENUM=[
   ('text','text'),
   ('audio','audio'),
   ('image','image'),
   ('video','video'),
   ('file','file'),
]

class ChatMessage(models.Model):
  message_type=models.CharField(max_length=30,default="text",choices=MESSAGE_ENUM)
  message=models.CharField(max_length=255,null=True,default="")
  read_by=models.CharField(max_length=255,default=[])
  sender_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="message_sender")
  chat_id=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="chat")
  created_at = models.DateTimeField(auto_now=True)
  isreaded=models.BooleanField(default=False)
  updated_at = models.DateTimeField(auto_now_add=True)

class FileAttachment(models.Model):
  chatmessage=models.ForeignKey(ChatMessage,on_delete=models.CASCADE,related_name="chatmessage")
  message_type=models.CharField(max_length=30,choices=MESSAGE_ENUM)
  attachment=models.FileField(max_length=255,null=True,upload_to="chat")
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)