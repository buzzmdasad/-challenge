from django.db import models
from user.models import UserDetails

class JobDetails(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    experience = models.CharField(max_length=255)
    work_location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    about_company = models.TextField()
    website = models.URLField()
    openings = models.IntegerField()
    no_of_applicants = models.IntegerField(default=0)
    application_deadline = models.DateField()
    recruiter = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='job_posts')

    def __str__(self):
        return self.job_title

class ApplicantDetails(models.Model):
    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='applicants')
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    applicant = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.applicant_name} - {self.job_title}'
