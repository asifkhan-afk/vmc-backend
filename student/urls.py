from django.urls import path
from .views import *
urlpatterns = [
    
 path('stprofile/',StudentProfileView.as_view(),name='StudentProfile'),
path('stprofile/<int:pk>/',StudentProfileView.as_view(),name='StudentProfile'),


path('education/<int:stid>/',EducationView.as_view() ,name='education'),
path('<int:eduid>/education/',EducationView.as_view() ,name='education'),

path('experience/<int:stid>/',WorkExperienceView.as_view() ,name='experience'),
path('<int:eduid>/experience/',WorkExperienceView.as_view() ,name='experience'),
   
]