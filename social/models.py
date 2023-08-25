from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True,null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower','following'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
         return f"{self.follower.first_name} follows {self.following.first_name}"
                


    def save(self, *args, **kwargs):
        if self.follower.pk != self.following.pk:  # preventing of following themselves
            return super().save(*args, **kwargs)



















# class Media(models.Model):
#     post=models.ForeignKey("Post",on_delete=models.CASCADE,related_name='media')
#     # file=models.FileField(upload_to="postmedia",default="images/default.jpg")
#     file=models.FileField(upload_to="posts")

TYPE=(
    ("question","Question"),
    ("general","General")
)
class Post(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userposts')
    # file = models.ForeignKey(Media,on_delete=models.CASCADE)
    file=models.FileField(upload_to="posts", null=True,blank=True)
    caption = models.CharField(max_length=255,null=True,blank=True)
    type=models.CharField(max_length=10,choices=TYPE,default="general")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    @property
    def is_retweet(self):
        return self.parent != None

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name}'s Post{self.caption}"

    def get_like_count(self):
        return self.postlikes.count()
    
    def get_comment_count(self):
        return self.comments.count()
    
    
    
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likedposts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postlikes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]
    def __str__(self):
        return f"{self.user.first_name} likes "
    

    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    file=models.FileField(upload_to="commentsphotos", null=True,blank=True)
    caption = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.first_name} commented on {self.post.caption}: {self.caption}"
    class Meta:
        ordering=['-created_at']
    


NOTIFICATION_STATUS=[
   ('read','read'),
   ('unread','unread'),
]

class Notification(models.Model):
    user_id = models.CharField(max_length=255)
    image=models.ImageField(upload_to ='notifications/',default="images/21.jpg")
    name = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS,null=False, default='unread')
    receiver_id = models.TextField(default="[]", null=True, blank=True)
    read_by = models.TextField(default="[]", null=True, blank=True)
    deleted_for = models.TextField(default="[]", null=True, blank=True)
    # notification_type= models.CharField(max_length=30, choices=NOTIFICATION_TYPE,null=False, default='')
    # receiver_id = models.CharField(default="[]",max_length=255,null=True,blank=True)
    # read_by = models.CharField(max_length=255,default="[]",null=True,blank=True)
    # deleted_for=models.CharField(max_length=255,default="[]",null=True,blank=True)

    
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
      return self.name

    class Meta:
      db_table="notifications"
      verbose_name="Notification"







    
# # class Share(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
# #     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
# #     created_at = models.DateTimeField(auto_now_add=True)
    
# #     def __str__(self):
# #         return f"{self.user.first_name} shared {self.post.text}"