
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Chat,ChatMessage,FileAttachment
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import ChatUserSerilizer,ChatSerilizer,ChatMessageSerilizer
import base64
from django.db import transaction
from django.core.files.base import ContentFile
import datetime 
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def chat_users(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            chat_user=User.objects.get(pk=pk)
            serializer=ChatUserSerilizer(chat_user)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
    
        if request.GET.get("user_name") and request.GET.get("login_id"):
            all_chat_users=User.objects.filter(Q(first_name__icontains=request.GET.get("user_name")) | Q(last_name__icontains=request.GET.get("user_name"))).exclude(pk=request.GET.get("login_id"))
            # all_chat_users=User.objects.filter(Q(first_name__icontains=request.GET.get("user_name")) | Q(last_name__icontains=request.GET.get("user_name")))
            serializer=ChatUserSerilizer(all_chat_users,many=True)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
        
    
        
        
        
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def chats(request,pk=None):
    if request.method=='GET':
        if request.GET.get("delete_message"):

            ChatMessage.objects.filter(pk=request.GET.get("delete_message")).delete()
            data = {
                "status_code": 200,
                "message": "Chat Message Deleted",
                }
            return Response(data)
        
        if request.GET.get("login_id"):
            # all_chat_users=User.objects.exclude(pk=request.GET.get("login_id")).filter(Q(first_name__icontains=request.GET.get("user_name")) | Q(last_name__icontains=request.GET.get("user_name")))
            chats=Chat.objects.filter(Q(sender_id__pk=request.GET.get("login_id")) | Q(reciever_id__pk=request.GET.get("login_id")))
            serializer=ChatSerilizer(chats,many=True)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
        
        
        if request.GET.get("chat_id") and request.GET.get("login_user"):
            chat_messages=ChatMessage.objects.filter(Q(sender_id=request.GET.get("login_user")) and Q(chat_id=request.GET.get("chat_id")))
            serializer=ChatMessageSerilizer(chat_messages,many=True)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
        
        if request.GET.get("sender_id") and request.GET.get("name"):
            chats=Chat.objects.filter(Q(sender_id__pk=request.GET.get("sender_id")) | Q(reciever_id__pk=request.GET.get("sender_id"))).filter(Q(reciever_id__first_name__icontains=request.GET.get("name")) | Q(reciever_id__last_name__icontains=request.GET.get("name")))
            serializer=ChatSerilizer(chats,many=True)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
        
        if request.GET.get("sender_id"):
            chats=Chat.objects.filter(Q(sender_id__pk=request.GET.get("sender_id")) | Q(reciever_id__pk=request.GET.get("sender_id")))
            serializer=ChatSerilizer(chats,many=True)
            data = {
                "status_code": 200,
                "message": "Chat Users",
                "data": serializer.data
                }
            return Response(data)
        
        if request.GET.get("search_chat_user") and request.GET.get("login_user"):
            print('mmmmmmmmmmmmmm',request.GET.get("search_chat_user"))
            print('tttttttttttttttttttt',request.GET.get("login_user"))

            chats=Chat.objects.filter(Q(Q(sender_id__pk=request.GET.get("login_user")) & Q(reciever_id__pk=request.GET.get("search_chat_user"))) | Q(Q(sender_id__pk=request.GET.get("search_chat_user")) & Q(reciever_id__pk=request.GET.get("login_user"))))
            if len(chats)>0:
                chat_messages=ChatMessage.objects.filter(Q(sender_id=request.GET.get("login_user")) and Q(chat_id=chats[0].id))
                serializer=ChatMessageSerilizer(chat_messages,many=True)
                data = {
                    "status_code": 200,
                    "message": "Chat Users",
                    "data": serializer.data
                    }
                return Response(data)
            return Response([])
        
        
        
        
        if pk is not None:
            chat_user=Chat.objects.get(pk=pk)
            serializer=ChatSerilizer(chat_user)
            data = {
                "status_code": 200,
                "message": "Chat",
                "data": serializer.data
                }
            return Response(data)
           
    if request.method=='POST':
        videos_extension = ["avi", "mp4", "mpeg", "webm"]
        audio_extension = ["aac", "mp3", "weba"]
        documents_extension = ["ppt", "pptx", "pdf", "docx", "doc"]
        image_extension = ["png", "jpg", "jpeg", "JPEG"]
            
        sender_id=User.objects.get(pk=request.data['sender_id'])
        reciever_id=User.objects.get(pk=request.data['reciever_id'])
        chat={}
        if Chat.objects.filter((Q(sender_id__pk=request.data['sender_id']) & Q(reciever_id__pk=request.data['reciever_id'])) | (Q(reciever_id__pk=request.data['sender_id']) & Q(sender_id__pk=request.data['reciever_id']))).exists():
            chat=Chat.objects.get((Q(sender_id__pk=request.data['sender_id']) & Q(reciever_id__pk=request.data['reciever_id'])) | (Q(reciever_id__pk=request.data['sender_id']) & Q(sender_id__pk=request.data['reciever_id'])))
        else:
            chat=Chat.objects.create(sender_id=sender_id,reciever_id=reciever_id)
        message=ChatMessage.objects.create(message=request.data['message'],sender_id=sender_id,chat_id=chat)
        list_of_files=[]
        if "file" in request.data:
            if message.message=='undefined':
                message.message=""
                message.save()
            format, imgstr = request.data['file'].split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            FileAttachment.objects.create(chatmessage=message,attachment=data,message_type="image")
            last_object=FileAttachment.objects.filter().last()
            chat.last_message_id=str(last_object.message_type).capitalize()
            chat.last_message_created_date=datetime.datetime.now()
            chat.save()
            data = {
                "status_code": 200,
                "message": "Files have been inserted",
                }
            return Response(data)

        if "vedioFile" in request.data:
            message.message=""
            message.save()
            print("vedioFile",request.data['vedioFile'])
            FileAttachment.objects.create(chatmessage=message,attachment=request.data['vedioFile'],message_type="vedio")
            data = {
                "status_code": 200,
                "message": "Audio have been inserted",
                }
            return Response(data)

        if "audioFile" in request.data:
            message.message=""
            message.save()
            print("audioFile",request.data['audioFile'])
            FileAttachment.objects.create(chatmessage=message,attachment=request.data['audioFile'],message_type="audio")
            data = {
                "status_code": 200,
                "message": "Audio have been inserted",
                }
            return Response(data)
        type=""
        if 'files_length' in request.data:
            for file in range(0,int(request.data['files_length'])):
                filename = str(request.FILES["path"+str(file)])
                print(filename)
                extension = filename.split(".").pop()
            
                if videos_extension.__contains__(extension):
                    type="vedio"
                elif audio_extension.__contains__(extension):
                    type="audio"
                elif documents_extension.__contains__(extension):
                    type="document"
                elif image_extension.__contains__(extension):
                    type="image"
                else:
                    print()


                list_of_files.append(FileAttachment(chatmessage=message,attachment=request.FILES["path"+str(file)],message_type=type))
            FileAttachment.objects.bulk_create(list_of_files)
            last_object=FileAttachment.objects.filter().last()
            if last_object.message_type!="":

                # chat.last_message_id=str(last_object.attachment).split("/").pop()
                chat.last_message_id=str(last_object.message_type).capitalize()
                chat.last_message_created_date=datetime.datetime.now()
                chat.save()
                data = {
                "status_code": 200,
                "message": "Files have been inserted",
                }
                return Response(data)
        
        else:
            chat.last_message_id=message.message
            chat.last_message_created_date=datetime.datetime.now()
            chat.save()
            data = {
            "status_code": 200,
            "message": "Files have been inserted",
            }
            return Response(data)
        
    if request.method=='DELETE':
        # if request.GET.get("type")=="message":
        #     ChatMessage.objects.filter(pk=pk).delete()
        #     data = {
        #         "status_code": 200,
        #         "message": "Message Deleted",
        #         }
        #     return Response(data)
        if request.GET.get('type')=="message":
                chat=Chat.objects.get(pk=request.GET.get('chat_id'))
                chatmessage=ChatMessage.objects.get(pk=pk)
                if len(chatmessage.chatmessage.all())>0:
                    chatmessage.message=""
                    chatmessage.save()
                else:
                    chatmessage.delete()
                message=ChatMessage.objects.filter().last()
                if message:
                    if len(message.chatmessage.all())>0:
                        last_file=message.chatmessage.last()
                        # chat.last_message_id=str(last_file.attachment).split("/").pop()
                        chat.last_message_id=str(last_file.message_type).capitalize()
                        chat.last_message_created_date=last_file.created_at
                        chat.save()
                    else:
                        chat.last_message_id=message.message
                        chat.last_message_created_date=message.created_at
                        chat.save()
                else:
                    chat.last_message_id=""
                    chat.last_message_created_date=datetime.datetime.now()
                    chat.save()
                data = {
                "status_code": 200,
                "message": "Message Deleted",
                    }
                return Response(data)
        
        if request.GET.get("type")=="file":
            # FileAttachment.objects.filter(pk=pk).delete()
            # data = {
            #     "status_code": 200,
            #     "message": "FileAttachment Deleted",
            #     }
            # return Response(data)
            chat=Chat.objects.get(pk=request.GET.get('chat_id'))
            chatmessage=ChatMessage.objects.get(chatmessage__pk=pk)
            FileAttachment.objects.get(pk=pk).delete()
            if len(chatmessage.chatmessage.all())==0 and chatmessage.message=="":
                chatmessage.delete()
            message=ChatMessage.objects.filter().last()
            if message:
                if len(message.chatmessage.all())>0:
                    last_file=message.chatmessage.last()
                    # chat.last_message_id=str(last_file.attachment).split("/").pop()
                    chat.last_message_id=str(last_file.message_type).capitalize()
                    chat.last_message_created_date=last_file.created_at
                    chat.save()
                else:
                    chat.last_message_id=message.message
                    chat.last_message_created_date=message.created_at
                    chat.save()
            else:
                chat.last_message_id=""
                chat.last_message_created_date=datetime.datetime.now()
                chat.save()
            data = {
                "status_code": 200,
                "message": "File Deleted",
              }
            return Response(data)
        return Response(serializer.errors)