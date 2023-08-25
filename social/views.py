import json
from django.shortcuts import render


from rest_framework .response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serilizers import PostSerializer
from rest_framework import viewsets
from django.contrib.auth import authenticate
# from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser,FormParser




#creating token manually
# from rest_framework_simplejwt.tokens import RefreshToken

def get_like_users(post_id):
  """Gets all the users who liked a given post."""
  likes = Like.objects.filter(post_id=post_id)
  users = []
  for like in likes:
   
    users.append(like.user.id)
    
  return users
# Create your views here.


from rest_framework import generics
from .models import Post

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .serilizers import *




from rest_framework.decorators import api_view, permission_classes

@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
def notifications(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            notification=Notification.objects.get(user__pk=pk)
            serializer=NotificationSerializer(notification)
            data = {
                "status_code": 200,
                "message": "Single Notication",
                "data": serializer.data,
                }
            return Response(data)
        # .exclude(Q(notification_type="meeting") | Q(notification_type="s_message"))
        if 1==1:
            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            #print(request.GET)
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

            user_id=request.user.id
            all_notification= Notification.objects.filter(receiver_id__contains=user_id).exclude(deleted_for__contains=user_id).order_by("-id")
            new_notification=all_notification.exclude(read_by__contains=user_id)
            # print(all_notification)
            all_notification_serializer=NotificationSerializer(all_notification,many=True)
            # student_id=request.GET.get("student")
            # unseen_notification=00
            # for index,_notification in enumerate(all_notification):
            #     users_id=json.loads(_notification.read_by)
            #     if student_id in users_id:
            #         unseen_notification+=1
            data = {
                "status_code": 200,
                "message": "Single Notication",
                "data": {"notifications":all_notification_serializer.data,"unread_messages":len(new_notification)},
                }
            return Response(data)
        
    



class NotificationView(APIView):
    # def get(self,request):
    #         user_id=request.user.id
    #         all_notification= Notification.objects.filter(receiver_id__contains=user_id).exclude(deleted_for__contains=user_id).order_by("-id")
    #         new_notification=all_notification.exclude(read_by__contains=user_id)
    #         # print(all_notification)
    #         all_notification_serializer=NotificationSerializer(all_notification,many=True)
    #         # student_id=request.GET.get("student")
    #         # unseen_notification=00
    #         # for index,_notification in enumerate(all_notification):
    #         #     users_id=json.loads(_notification.read_by)
    #         #     if student_id in users_id:
    #         #         unseen_notification+=1
    #         data = {
    #             "status_code": 200,
    #             "message": "Single Notication",
    #             "data": {"notifications":all_notification_serializer.data,"unread_messages":len(new_notification)},
    #             }
    #         return Response(data)
    def post(self, request, notificationid=None):
        n_obj = Notification.objects.get(pk=int(notificationid))
        userid = request.user.id
        if  'status' in request.data and request.data['status']=='readed':
            read_by = json.loads(n_obj.read_by)  # Convert read_by to a list
            read_by.append(userid)
            n_obj.read_by = json.dumps(read_by)  # Convert read_by back to a string
            n_obj.save()
        if  'delete' in request.data and request.data['delete'] == 'delete':
            deleted_for = json.loads(n_obj.deleted_for)  # Convert read_by to a list
            deleted_for.append(userid)
            n_obj.deleted_for= json.dumps(deleted_for)  # Convert read_by back to a string
            n_obj.save()

        data = {
            
            "status_code": 200,
            "message": "Notifications readed",
        }
        return Response(data)













class FollowView(APIView):
    def post(self, request):
        # follower_id = request.data.get('follower_id')
        following_id = request.data.get('following_id')
        #print(following_id,'following id')
        user = request.user
        following = get_object_or_404(User, pk=following_id)
        #print(following)
        #print(user)
        
        # check if the follower is not already following the user
        if Follow.objects.filter(follower=user, following=following).exists():
            #print('deleting like')
            Follow.objects.filter(follower=user, following=following).delete()
            return Response({'error': 'The follower was already following the user.'}, status=status.HTTP_204_NO_CONTENT)
        
        follow = Follow.objects.create(follower=user, following=following)
        #print("saving")
        follow.save()
        Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message="Started Following you",url=f"profile/{request.user.id}",receiver_id=[following_id])
       
        #print(" follow saved")

        # serializer = FollowSerializer(follow)

        return Response({'message':'follow has been saved'},status=status.HTTP_201_CREATED)
    
    def get(self, request, fid=None):
        if fid:
            user = request.user
            #print(user.id)
            #print('fid',fid)
            try:
                follow = Follow.objects.get(follower=user.id, following=fid)
                #print(request.user)
                #print(User.objects.get(id=fid))
                serilizer=FollowSerializer(follow)
                #print(serilizer.data)
                return Response(serilizer.data,status=status.HTTP_200_OK)
                
            except Follow.DoesNotExist:
                follow = None
                # serilizer=FollowersSerializer(follow)
                return Response({},status=status.HTTP_204_NO_CONTENT)
        
        return Response({},status=status.HTTP_204_NO_CONTENT)


# followres=Follow.objects.filter(follower=user)
#         #print(followres)
#         serilizer=FollowSerializer(followres)
#         #print(serilizer.data)
    # def delete(self, request, fid=None):
    #     #print(fid,'this is delete fid')
    #     follow = get_object_or_404(Follow, pk=fid)
    #     #print(follow,'this is elete follow')
    #     follow.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)















class CommentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, postid=None):
        if postid:
          post=get_object_or_404(Post,id=postid)
          #print(request.data)
          caption=request.data['caption']
          file = request.FILES.get('file') 
          
          if caption or file:
           
            serializer = CommentSerilizer(data=request.data)       
            if serializer.is_valid(raise_exception=True):
                #print("creating serilizer")
                serializer.save(user=self.request.user,post=post)
                if  post.user.id != request.user.id:
                    Notification.objects.create(user_id=request.user.id,image=request.user.profilepic,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message=f"Commented on your {post.type}",url=f"home/postdetail/{post.id}",receiver_id=[post.user.id])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
          return Response({'msg':'both file and caption cannot be none'})
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,postid=None,cmntid=None):
        if postid:
            post=get_object_or_404(Post,pk=postid).id
            cmnts=Comment.objects.filter(post=post) 
            serializer = PostSerializer(cmnts,many=True)
        else:
            cmnt=get_object_or_404(Comment,id=cmntid)
            serializer = CommentSerilizer(cmnt)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,cmntid=None): 
        if cmntid:
            #print("this is psorrrrrrrr",request.data)
            c=get_object_or_404(Comment,id=cmntid)
            #print('this is psorrrrrrrr',c)
            if c.user==request.user:
                serilizer=CommentSerilizer(instance=c, data=request.data, partial=True)
                
                if serilizer.is_valid():
                    #print("put seriiiiiiii for comment",serilizer.validated_data)
                    serilizer.save()
                    #print(serilizer.data)
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response('post id is messing')
    
    def delete(self,requset,cmntid=None):
        if cmntid:
            p=get_object_or_404(Comment,id=cmntid)
            if requset.user==p.user:
                 p.delete()
                 return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        




class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)   
        #print(request.data)     
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            #print("creating notification")
            # #print(request.user.get_following())
            followers=request.user.get_followers()
            followers_id=[]
            for i in followers:
                followers_id.append(i.follower.id)
                #print(followers_id)
            # #print(serializer.data['user'])
            Notification.objects.create(user_id=request.user.id,name=f'{request.user.first_name} {request.user.last_name if request.user.last_name else ""}' ,message=" Shared a new post ",url=f"home/postdetail/{serializer.data['id']}",receiver_id=followers_id)
            #print("created noti ")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, userid=None, postid=None):
        if userid:
            user = get_object_or_404(User, pk=userid)
            posts = Post.objects.filter(user=user)
            serializer = PostSerializer(posts, many=True)
            data=serializer.data.copy()

            for post in data:
                like_users = get_like_users(post['id'])
                post['like_users'] = like_users

        if postid:
            post = get_object_or_404(Post, id=postid)
            
            serializer = PostSerializer(post)
            like_users = get_like_users(post.id)
            data=serializer.data.copy()
            data['like_users'] = like_users
        return Response(data, status=status.HTTP_200_OK)


    def put(self,request,postid=None):
        #print(postid)
        if postid:
            #print("this is psorrrrrrrr",request.data)
            p=get_object_or_404(Post,id=postid)
            #print('this is psorrrrrrrr',p)
            if p.user==request.user:
                serilizer=PostSerializer(instance=p, data=request.data, partial=True)
                
                if serilizer.is_valid():
                    #print("put seriiiiiiii",serilizer.validated_data)
                    serilizer.save()
                    #print(serilizer.data)
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response('post id is messing')
    
    def delete(self,requset,postid=None):
        if postid:
            p=get_object_or_404(Post,id=postid)
            if requset.user==p.user:
                 
                 p.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        


class PostListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # Iterate over the posts and add like_users to each post's data
        for post_data in serializer.data:
            like_users = get_like_users(post_data['id'])
            post_data['like_users'] = like_users
        return Response(serializer.data)

class LikeView(APIView):
    def post(self,request,userid=None,postid=None):
        #print(postid,userid)
        if userid and postid:
            user=get_object_or_404(User,id=userid)
            #print(user)
            post=get_object_or_404(Post,id=postid)
            #print(post)
            if request.user==user:
                like=Like.objects.create(user=user,post=post)
                like.save()
                return Response({'msg':'liked'},status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get(self, request, userid=None, postid=None):
        likes =Like.objects.filter(post_id=postid)
        #print("these are lieks ",likes)
        for like in likes:
            if like.user_id == userid:
                like_status = like.like_status
                break
        else:
            like_status = None

        if like_status is None:
            return Response({'like_status': 'unliked'})
        else:
            return Response({'like_status': like_status})
    def delete(self,request, postid=None,userid=None):
        if userid and postid:
            like = get_object_or_404(Like, user_id=userid, post_id=postid)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        # like = get_object_or_404(Like, post_id=postid)
        # #print(like)
         

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # like.delete()
