from django.urls import path
from .views import *

urlpatterns = [
    path('notifications/',notifications,name='notifications'),
    path('notifications/<int:pk>',notifications,name='notifications'),
    path('<int:notificationid>/notification/',NotificationView.as_view(),name='notifications'),






    path("follow/",FollowView.as_view(),name='folllow'),
    path("follow/<int:fid>/",FollowView.as_view(),name='folllow'),
 path('post/',PostView.as_view(),name="create_post"),
 path('post/<int:userid>/',PostView.as_view(),name="create_post"),
 path('<int:postid>/postupdel/',PostView.as_view(),name="post"),
 path('postlist/',PostListView.as_view(),name="postlist"), 

 path('<int:postid>/like/<int:userid>/',LikeView.as_view(),name='like'),
#  path('<int:likeid>/dellike',LikeView.as_view(),name="dellike"),

  path('<int:cmntid>/comment/<int:postid>/',CommentView.as_view(),name="cmntview"),
   path('<int:cmntid>/comment/',CommentView.as_view(),name="cmntupdate"),
 path('comment/<int:postid>/',CommentView.as_view(),name="create_post"),
 path('<int:cmntid>/comment/',CommentView.as_view(),name="post"),
]