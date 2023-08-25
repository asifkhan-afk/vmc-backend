from django.urls import path
from .views import *
urlpatterns = [
    path('doctors/',DrSearchView.as_view(),name='drsearch'),
    path('students/',StSearchView.as_view(),name='stsearch'),
    path('patients/',PtSearchView.as_view(),name='ptsearch'),
    path('hospitals/',HsSearchView.as_view(),name='hssearch'),
    path('research/',ResearchSearchView.as_view(),name='research'),
    path('jobs/',JobSearchView.as_view(),name='jobs'),

]