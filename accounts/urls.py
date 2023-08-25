from django.urls import path,include
from accounts.views import *
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)


urlpatterns=[
path("token/", TokenView.as_view(), name="access_token"),
path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
path('register/',UserRegestrationView.as_view(),name='register'),
path('register/<int:userid>/',UserRegestrationView.as_view(),name='register'),

# path('login/',UserLoginView.as_view(),name='login'),
path('logout/',UserLogOut.as_view(),name='logout'),
 path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
path('changepassword/',UserChangePassword.as_view(),name='changepassword'),
path('emailresetpassword/',EmailResetPasswordView.as_view(),name='emailresetpassword'),
path('resetpassword/<uid>/<token>/',ResetPasswordView.as_view(),name='resetpassword'),
path("userlist/<int:userid>/", Userlistview.as_view(), name="userlist"),
path("userlist/", Userlistview.as_view(), name="userlist"),






]