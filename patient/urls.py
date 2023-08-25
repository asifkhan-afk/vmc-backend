from django.urls import path
from .views import *
urlpatterns = [
    path('patientprofile/',PatientProfileView.as_view(),name='patientprofile'),
path('patientprofile/<int:pk>/',PatientProfileView.as_view(),name='patientprofile'),
path('questionare/',QuestionareView.as_view(),name='questionare'),
# path('aiquestionare/',AIQuestionareView.as_view(),name='aiquestionare'),



]