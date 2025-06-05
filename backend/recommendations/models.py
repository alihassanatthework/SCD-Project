from django.db import models
from accounts.models import User, JobSeekerProfile
from jobs.models import JobPosting

class JobRecommendation(models.Model):
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(default=0.0)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_seeker', 'job')
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"Recommendation for {self.job_seeker.user.username}: {self.job.title}"

class UserActivityLog(models.Model):
    ACTIVITY_TYPES = (
        ('view_job', 'Viewed Job'),
        ('apply_job', 'Applied to Job'),
        ('wishlist_job', 'Added to Wishlist'),
        ('search', 'Performed Search'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, null=True, blank=True)
    search_query = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"