from django.urls import path
from .views import (
    JobPostView, MyPostsView, JobStatusView, ViewProfileView,
    JobUpdateDeleteView, JobListView, JobFiltersView, JobApplyView, JobAppliedView
)

urlpatterns = [
    path('postjob/', JobPostView.as_view(), name='postjob'),
    path('myposts/', MyPostsView.as_view(), name='myposts'),
    path('jobstatus/<int:job_id>/', JobStatusView.as_view(), name='jobstatus'),
    path('viewprofile/<int:applicant_id>/', ViewProfileView.as_view(), name='viewprofile'),
    path('updatejob/<int:pk>/', JobUpdateDeleteView.as_view(), name='updatejob'),
    path('listjob/', JobListView.as_view(), name='listjob'),
    path('filterjob/', JobFiltersView.as_view(), name='filterjob'),
    path('applyjob/', JobApplyView.as_view(), name='applyjob'),
    path('appliedjobs/', JobAppliedView.as_view(), name='appliedjobs'),
]
