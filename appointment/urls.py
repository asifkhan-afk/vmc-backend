from django.urls import path
from .views import AppointmentView,Availableslots


urlpatterns = [
    path('<int:appid>/appointment/',AppointmentView.as_view(),name='appointment'),
    path('appointment/<int:drid>/',AppointmentView.as_view(),name='appointment'),
    path('ptappointment/<int:ptid>/',AppointmentView.as_view(),name='appointment'),
path('slots/<int:drid>/', Availableslots.as_view(), name='appointment'),
    
]