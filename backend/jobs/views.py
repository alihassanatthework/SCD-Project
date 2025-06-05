
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import JobCategory, JobPosting, JobApplication, JobWishlist
from .serializers import (
    JobCategorySerializer, JobPostingSerializer, JobPostingCreateSerializer,
    JobApplicationSerializer, JobApplicationCreateSerializer, JobWishlistSerializer
)

class JobCategoryListView(generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.AllowAny]

class JobPostingListView(generics.ListAPIView):
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'employment_type', 'experience_level', 'location']
    search_fields = ['title', 'description', 'requirements', 'skills_required']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    ordering = ['-created_at']

class JobPostingDetailView(generics.RetrieveAPIView):
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class JobPostingCreateView(generics.CreateAPIView):
    serializer_class = JobPostingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer_profile)

class JobPostingUpdateView(generics.UpdateAPIView):
    serializer_class = JobPostingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobPosting.objects.filter(employer=self.request.user.employer_profile)

class JobPostingDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobPosting.objects.filter(employer=self.request.user.employer_profile)

class EmployerJobsView(generics.ListAPIView):
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobPosting.objects.filter(employer=self.request.user.employer_profile)

class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.job_seeker_profile)

class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'job_seeker':
            return JobApplication.objects.filter(applicant=user.job_seeker_profile)
        elif user.user_type == 'employer':
            return JobApplication.objects.filter(job__employer=user.employer_profile)
        return JobApplication.objects.none()

class JobApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'job_seeker':
            return JobApplication.objects.filter(applicant=user.job_seeker_profile)
        elif user.user_type == 'employer':
            return JobApplication.objects.filter(job__employer=user.employer_profile)
        return JobApplication.objects.none()

@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def wishlist_toggle(request, job_id):
    try:
        job = JobPosting.objects.get(id=job_id, is_active=True)
        job_seeker = request.user.job_seeker_profile
        
        if request.method == 'POST':
            wishlist_item, created = JobWishlist.objects.get_or_create(
                job_seeker=job_seeker,
                job=job
            )
            if created:
                return Response({'message': 'Job added to wishlist'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Job already in wishlist'}, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            try:
                wishlist_item = JobWishlist.objects.get(job_seeker=job_seeker, job=job)
                wishlist_item.delete()
                return Response({'message': 'Job removed from wishlist'}, status=status.HTTP_200_OK)
            except JobWishlist.DoesNotExist:
                return Response({'message': 'Job not in wishlist'}, status=status.HTTP_404_NOT_FOUND)
    
    except JobPosting.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

class WishlistView(generics.ListAPIView):
    serializer_class = JobWishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobWishlist.objects.filter(job_seeker=self.request.user.job_seeker_profile)
