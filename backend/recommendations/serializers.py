
from rest_framework import serializers
from .models import JobRecommendation
from jobs.serializers import JobPostingSerializer

class JobRecommendationSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)
    
    class Meta:
        model = JobRecommendation
        fields = '__all__'
