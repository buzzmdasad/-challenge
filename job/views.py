from rest_framework import generics, authentication, permissions, status
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from job.models import  JobDetails, ApplicantDetails
from job.serializers import  JobSerializer, ApplicantSerializer
from django.contrib.auth import get_user_model, authenticate
from user.models import UserDetails
from user.serializers import UserSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Method to post a job
# className ---> JobPostView
class PostJobView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    def post(self, request):
        #print('post job'+request.user.company)
        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        job_data = request.data.copy()
        job_data['company'] = request.user.company
        job_data['website'] = request.user.website
        job_data['about_company'] = request.user.about_company
        serializer = JobSerializer(data=job_data)
        if serializer.is_valid():
            job = serializer.save(recruiter=self.request.user)
            return Response({'message': 'job details have been posted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Method to view the recruiter job posts
# className --->  MyPostsView
class MyPostsView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    def get(self, request):
        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        jobs = JobDetails.objects.filter(recruiter=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# Method to view the job status
# className --->  JobStatusView
class JobStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        try:
            job = JobDetails.objects.get(id=job_id, recruiter=request.user)
        except JobDetails.DoesNotExist:
            return Response({'message': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        applicants = ApplicantDetails.objects.filter(job=job)
        data = [{
            'job_id': job.id,
            'job_title': job.job_title,
            'company': job.company,
            'applicant_id': app.applicant.id,
            'applicant_name': app.applicant.name,
            'applicant_email': app.applicant.email
            } for app in applicants]

        return Response(data)


# Method to view seeker profile
# className --->  ViewProfileView

class ViewProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request, applicant_id):
        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        try:
            applicant = UserDetails.objects.get(id=applicant_id)
        except UserDetails.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(applicant)
        return Response(serializer.data)


#Method to update and delete a job
#className --->  JobUpdateDeleteView
#Create a permission to allow recruiters to edit only their own job post details
class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset = JobDetails.objects.all()
    serializer_class = JobSerializer

    def patch(self, request, pk):
        # Check if the user is not a staff member (or not a recruiter if you have that distinction)
        if not request.user.is_authenticated:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)

        try:
            job = JobDetails.objects.get(id=pk)
        except JobDetails.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        if job.recruiter != self.request.user:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'job details have been updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        try:
            job = JobDetails.objects.get(id=pk, recruiter=request.user)
        except JobDetails.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'job details have been updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        if not request.user.is_staff:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            job = JobDetails.objects.get(id=pk, recruiter=request.user)
        except JobDetails.DoesNotExist:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = JobDetails.objects.all()
#     serializer_class = JobSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         # Get the job object by primary key (pk) from the URL kwargs
#         pk = self.kwargs.get('pk')
#         #job = self.get_object(JobDetails, id=pk)
#         job= JobDetails.objects.get(id=pk)
#         if job is None:
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
#         # Check if the user is the recruiter who posted the job
#         if job.recruiter != self.request.user:
#             raise PermissionDenied("You do not have permission to perform this action.")
#
#         return job
#     def get(self, request, *args, **kwargs):
#         # Overriding to handle the response with authentication check
#         if not request.user.is_authenticated:
#             return Response({'detail': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
#         return super().get(request, *args, **kwargs)

# Method to list all the jobs
# className --->  JobListView

class ListJobView(APIView):
   def get(self, request):
       jobs = JobDetails.objects.all()
       serializer = JobSerializer(jobs, many=True)
       return Response(serializer.data)

# Method to filter jobs
# className --->  JobFiltersView
class FilterJobView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')
        jobs = JobDetails.objects.filter(
            Q(job_title__icontains=search_query) |
            Q(work_location__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# Method to apply for a job
# className --->  JobApplyView

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantSerializer
    def post(self, request):
        if request.user.is_staff:
            return Response({'message': 'You need seeker privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        job_id = request.data.get('job_id')
        try:
            job = JobDetails.objects.get(id=job_id)
        except JobDetails.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        applicant, created = ApplicantDetails.objects.get_or_create(
            job=job,
            applicant=self.request.user,
            defaults={
                'job_title': job.job_title,
                'company': request.user.company,
                'applicant_name': request.user.name,
                'applicant_email': request.user.email,
                'applicant_id' : request.user.id,
            }
        )
        if created:
            job.no_of_applicants += 1
            job.save()
            return Response({'message': 'You have successfully applied for this job'})
        return Response({'message': 'You have already applied for this job'},status=status.HTTP_406_NOT_ACCEPTABLE)

# Method to view seeker applied jobs
# className --->  JobAppliedView

class AppliedJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            return Response({'message': 'You need seeker privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        applications = ApplicantDetails.objects.filter(applicant=request.user)
        data = [
            {
                'job_id': app.job.id,
                'job_title': app.job.job_title,
                'company': app.job.company,
                'applicant_id': app.applicant.id,
                'applicant_name': app.applicant.name,
                'applicant_email': app.applicant.email
            }
            for app in applications
        ]

        return Response(data)
