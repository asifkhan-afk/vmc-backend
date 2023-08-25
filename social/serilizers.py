
from rest_framework import serializers
from .models import *
from accounts.serilizers import UserSerializer
# from django.utils import timezone
# from django.utils.timesince import timesince



class NotificationSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True, format="%A, %d. %B %Y %I:%M%p")
    created_at = serializers.DateTimeField(read_only=True, format="%A, %d %B %Y, %I:%M %p")
    class Meta:
        model=Notification
        fields="__all__"

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ("id", "following", "created")

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "created")









class CommentSerilizer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields = '__all__'
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     created_at = instance.created_at

    #     # Format the time and date separately
    #     time = created_at.strftime("%I:%M %p")  # Format time as 12-hour clock
    #     date = created_at.strftime("%B %d, %Y")  # Format date as Month day, Year


class CommentSeri(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields = ['id','user','file','caption','created_at'] 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_at = instance.created_at

        # Format the time and date separately
        time = created_at.strftime("%I:%M %p")  # Format time as 12-hour clock
        date = created_at.strftime("%B %d, %Y")  # Format date as Month day, Year
        representation['created_at'] = {
            'time': time,
            'date': date,
        }
        return representation
    def validate(self, data):
        caption = data.get('caption')
        file = data.get('file')

        if not caption and not file:
            raise serializers.ValidationError("Both caption and file cannot be null at the same time.")






class LikeSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields = '__all__' 
        unique_together = ('user', 'post')  

   

class PostSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    comments=CommentSeri(read_only=True,many=True)
    
    
    
 

    class Meta:
        model = Post                
                                               
        fields = ['id','user', 'caption','created_at','updated_at', 'type','file','like_count','comments','comment_count']  
        extra_kwargs = {
            'caption': {'allow_null': True, 'required': False},
            'file': {'allow_null': True, 'required': False},
        }
    # def prefetch_comments(self, queryset):
    #     queryset = queryset.prefetch_related('comments')
    #     return queryset
    
    def validate(self, data):
        caption = data.get('caption')
        file = data.get('file')

        if not caption and not file:
            raise serializers.ValidationError("Both caption and file cannot be null at the same time.")

        return data
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_at = instance.created_at

        # Format the time and date separately
        time = created_at.strftime("%I:%M %p")  # Format time as 12-hour clock
        date = created_at.strftime("%B %d, %Y")  # Format date as Month day, Year

        # Add time and date to the representation
        representation['created_at'] = {
            'time': time,
            'date': date,
        }

        return representation
    def get_url(self,obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def get_like_count(self,obj):
        return obj.get_like_count()
    
    def get_comment_count(self,obj):
        return obj.get_comment_count()
    
    
    

   