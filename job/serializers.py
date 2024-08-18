from rest_framework import serializers
from .models import JobDetails, ApplicantDetails

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDetails
        fields = '__all__'
