from django import urls
from django.urls import path
from .views import *

urlpatterns = [
path('hospitalprofile/',HospitalProfileView.as_view(),name='HospitalProfile'),
path('hospitalprofile/<int:pk>/',HospitalProfileView.as_view(),name='HospitalProfil'),
path('gethospitalprofile/',GetHospitalProfileView.as_view(),name='GetHospitalProfile'),
path('gethospitalprofile/<int:pk>/',GetHospitalProfileView.as_view(),name='GetHospitalProfil'),

 path('<int:hsid>/galleries/', GalleryApiView.as_view(), name=''),
 path('galleries/<int:id>/', GalleryApiView.as_view(), name=''),

path('apply/<int:jobid>/',ApplyView.as_view(),name='apply'),
path('<int:applyid>/updateapply/',ApplyView.as_view(),name='apply'),



path('<int:hsid>/hospitaldepartments/',HospitalDepartmentView.as_view(),name='hospitaldepartments'),
path('hsdpt/<int:id>/',HospitalDepartmentView.as_view(),name='hospitaldepartment'),


path('<int:hsid>/hospitalservices/',HospitalServicesView.as_view(),name='hospitalserviceses'),
path('service/<int:id>/',HospitalServicesView.as_view(),name='hospitalservices'),

path('<int:hsid>/afdoctor/',AffiliatedDoctorsView.as_view(),name='afdoctor'),
path('afdoctor/<int:afdid>/',AffiliatedDoctorsView.as_view(),name='afdoctor'),

path('hsjob/<int:jobid>/',HospitalJobView.as_view(),name='Hospitaljob'),
path('<int:hsid>/hsjob/',HospitalJobView.as_view(),name='job'),
path('hsalljob/',JobListView.as_view(),name='joblist'),
]