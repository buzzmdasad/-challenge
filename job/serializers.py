from rest_framework import serializers
from .models import JobDetails, ApplicantDetails

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = ['id', 'job_title', 'company', 'description', 'experience', 'work_location', 'employment_type', 'qualification', 'about_company', 'website', 'openings', 'no_of_applicants', 'application_deadline']


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDetails
        fields = ['id', 'job_id', 'job_title', 'company', 'applicant_id', 'applicant_name', 'applicant_email']
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # Remove keys with None values
    #     return {key: value for key, value in representation.items() if value is not None}
