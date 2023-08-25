"""
URL configuration for vmc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns





urlpatterns = [
    path('admin/', admin.site.urls),
     path('api-auth/', include('rest_framework.urls')),
    # path('auth/', include('djoser.urls')),
    #  path('auth/', include('djoser.urls.jwt')),
    path('api/user/',include('accounts.urls')),
    path('api/doctor/',include('doctor.urls')),
    path('api/patient/',include('patient.urls')),
    path('api/student/',include('student.urls')),
    path('api/hospital/',include('hospital.urls')),
    path('api/social/',include('social.urls')),
    path('api/search/',include('searchapp.urls')),
    path('api/',include('chat.urls')),
    path('api/appointment/',include('appointment.urls')),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()