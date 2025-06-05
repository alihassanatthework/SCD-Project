
from rest_framework import generics, permissions
from .models import JobRecommendation
from .serializers import JobRecommendationSerializer

class JobRecommendationListView(generics.ListAPIView):
    serializer_class = JobRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobRecommendation.objects.filter(
            job_seeker=self.request.user.job_seeker_profile,
            job__is_active=True
        )[:10]
