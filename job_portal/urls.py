"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,
    )
from user.views import (
    RecruiterSignupView,SeekerSignupView,LoginView,RecruiterProfileView,LogoutView,SeekerProfileView,CreateTokenView,ManageUserView,
    )
from job.views import (
    PostJobView, MyPostsView, JobStatusView, ViewProfileView,JobUpdateDeleteView, ListJobView, FilterJobView, ApplyJobView, AppliedJobsView,

    )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('recruiter/signup/', RecruiterSignupView.as_view(), name='recruiter-signup'),
    path('seeker/signup/', SeekerSignupView.as_view(), name='seeker-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('recruiterprofile/', RecruiterProfileView.as_view(), name='recruiterprofile'),
    path('seekerprofile/', SeekerProfileView.as_view(), name='seekerprofile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CreateTokenView.as_view(), name='token'),
    ###job start###
    path('postjob/', PostJobView.as_view(), name='postjob'),
    path('myposts/', MyPostsView.as_view(), name='myposts'),
    path('jobstatus/<int:job_id>', JobStatusView.as_view(), name='jobstatus'),
    path('viewprofile/<int:applicant_id>', ViewProfileView.as_view(), name='viewprofile'),
    path('updatejob/<int:pk>', JobUpdateDeleteView.as_view(), name='updatejob'),
    path('listjob/', ListJobView.as_view(), name='listjob'),
    path('filterjob/', FilterJobView.as_view(), name='filterjob'),
    path('applyjob/', ApplyJobView.as_view(), name='applyjob'),
    path('appliedjobs/', AppliedJobsView.as_view(), name='appliedjobs'),
]
