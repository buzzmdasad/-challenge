from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JobDetails, ApplicantDetails
from .serializers import JobSerializer, ApplicantSerializer
from user.models import UserDetails
from rest_framework.permissions import IsAuthenticated

class JobPostView(generics.CreateAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class MyPostsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobDetails.objects.filter(recruiter=self.request.user)

class JobStatusView(generics.RetrieveAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobDetails.objects.filter(recruiter=self.request.user)

class ViewProfileView(generics.RetrieveAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDetails.objects.filter(id=self.kwargs['applicant_id'])

class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobDetails.objects.filter(recruiter=self.request.user)

class JobListView(generics.ListAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer

class JobFiltersView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = JobDetails.objects.all()
        job_title = self.request.query_params.get('job_title', None)
        work_location = self.request.query_params.get('work_location', None)
        company = self.request.query_params.get('company', None)
        description = self.request.query_params.get('description', None)
        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)
        if work_location:
            queryset = queryset.filter(work_location__icontains=work_location)
        if company:
            queryset = queryset.filter(company__icontains=company)
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset

class JobApplyView(generics.CreateAPIView):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job = JobDetails.objects.get(id=self.request.data.get('job_id'))
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(applicant=self.request.user, job_title=job.job_title, company=job.company)

class JobAppliedView(generics.ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApplicantDetails.objects.filter(applicant=self.request.user)
