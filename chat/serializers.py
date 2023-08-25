from rest_framework import serializers
from .models import Chat,ChatMessage,FileAttachment
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatUserSerilizer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True, format="%A, %d %B %Y, %I:%M %p")
    class Meta:
        model=User
        exclude=['password','is_active','is_staff','is_superuser','last_login',]


class ChatSerilizer(serializers.ModelSerializer):
    last_message_created_date=serializers.DateTimeField(read_only=True, format="%A, %d %B %Y, %I:%M %p")
    reciever_id=ChatUserSerilizer()
    sender_id=ChatUserSerilizer()
    class Meta:
        model=Chat
        fields='__all__'
        ordering=['-last_message_created_date']

class ChatPostSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Chat
        fields='__all__'

class FileAttachmentSerilizer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True, format="%A, %d %B %Y, %I:%M %p")
    class Meta:
        model=FileAttachment
        fields='__all__'

class ChatMessageSerilizer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True, format="%A, %d %B %Y, %I:%M %p")
    chatmessage=FileAttachmentSerilizer(many=True,read_only=True)
    class Meta:
        model=ChatMessage
        fields='__all__'