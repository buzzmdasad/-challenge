from django.urls import path
from .views import (
    PostJobView, MyPostsView, JobStatusView, ViewProfileView,
    JobUpdateDeleteView, ListJobView, FilterJobView, ApplyJobView, AppliedJobsView
)

urlpatterns = [
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
