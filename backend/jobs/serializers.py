
from rest_framework import serializers
from .models import JobCategory, JobPosting, JobApplication, JobWishlist, CandidateWatchlist
from accounts.serializers import EmployerProfileSerializer, JobSeekerProfileSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    employer = EmployerProfileSerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    applications_count = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPosting
        fields = '__all__'
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.user_type == 'job_seeker':
            return JobWishlist.objects.filter(job_seeker__user=request.user, job=obj).exists()
        return False

class JobPostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        exclude = ('employer', 'views_count', 'created_at', 'updated_at')

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = JobSeekerProfileSerializer(read_only=True)
    job = JobPostingSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('job', 'cover_letter', 'resume')

class JobWishlistSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)
    
    class Meta:
        model = JobWishlist
        fields = '__all__'

class CandidateWatchlistSerializer(serializers.ModelSerializer):
    candidate = JobSeekerProfileSerializer(read_only=True)
    
    class Meta:
        model = CandidateWatchlist
        fields = '__all__'
