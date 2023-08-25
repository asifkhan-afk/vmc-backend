from django.urls import path
from .views import *




urlpatterns = [


path('drprofilelist/',DrProfileList.as_view(),name='drprofilelist'),
path('drprofile/',DrProfileView.as_view(),name='drprofile'),
path('drprofile/<int:pk>/',DrProfileView.as_view(),name='profile'),
path('speciality/<int:drid>/',DrSpecialityView.as_view() ,name='speciality'),
path('<int:spid>/speciality/',DrSpecialityView.as_view() ,name='specialit'),

path('education/<int:drid>/',EducationView.as_view() ,name='education'),
path('<int:eduid>/education/',EducationView.as_view() ,name='education'),

path('experience/<int:drid>/',WorkExperienceView.as_view() ,name='experience'),
path('<int:eduid>/experience/',WorkExperienceView.as_view() ,name='experience'),

path('research/<int:resid>/',ResearchView.as_view(),name='research'),
# path('allresearch/',AllResearchView.as_view(),name='allresearch'),
path('<int:drid>/drres/',ResearchView.as_view(),name='drres'),
path('research/',ResearchView.as_view(),name='drres'),


path('researchappli/<int:researchid>/',ResearchApplyView.as_view(),name='resapply'),
path('<int:resapplyid>/researchappup/',ResearchApplyView.as_view(),name='resapply'),
path('<int:studentid>/stresapplist/',ResearchApplyView.as_view(),name='resapply'),

]