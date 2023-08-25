from django.urls import path,include
from . import views




urlpatterns = [
    path('users',views.chat_users,name="users"),
    path('users/<int:pk>',views.chat_users,name="users"),
    path('chats',views.chats,name="chats"),
    path('chats/<int:pk>',views.chats,name="chats"),
    
]