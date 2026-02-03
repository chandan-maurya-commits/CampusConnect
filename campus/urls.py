"""
URL configuration for campus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from student import views
# from .views import upload_attendance


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_user, name='log'),          # login page
    path('register/', views.register_user, name='register'),       # registration page
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('coordinator/dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('clubs/', views.clubs, name='clubs'),
    path('events_form/', views.events_form, name='events_form'),   
    path('placements/', views.placements, name='placements'),
    path('events/event_registration.html', views.event_registration, name='event_registration'),
    path('placements/placement_apply.html', views.placement_apply, name='placement_apply'),
    path('base/', views.base, name='base'),
    path('assignment/', views.assignment_form, name='assignment_form'),
    path('base2/', views.base2, name='base2'),
    path('club_form/' , views.club_form, name='club_form'),
    path('place_form/' , views.place_form , name = 'place_form'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('add_club/' , views.add_club , name = "add_club"),
    path('add_event/', views.add_event, name='add_event'),
    path('add-placement-drive/', views.add_placement_drive, name='add_placement_drive'),
    path('std_assingment/', views.std_assignment , name = 'std_assignment'),
    path('events/' , views.events , name="events"),
    path('profile/' , views.profile , name = "profile"),
    path('about/', views.about , name = 'about'),
    path('logout/' , views.lout , name = 'lout'),
    path('st_profile/' , views.st_profile , name = 'st_profile'),
    path("upload-attendance/", views.upload_attendance, name="upload_attendance"),
    path("my-attendance/", views.student_attendance, name="student_attendance"),
    path('upload-results/', views.upload_results, name='upload_results'),
    path('results/', views.results , name = 'results')

    

    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

