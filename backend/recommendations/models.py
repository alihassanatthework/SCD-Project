from django.db import models
from accounts.models import User, JobSeeker, Employer
from jobs.models import JobPosting

class JobRecommendation(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='job_recommendations')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='recommendations')
    match_score = models.FloatField()
    is_viewed = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job_seeker', 'job')
    
    def __str__(self):
        return f"Job recommendation for {self.job_seeker.user.username} - {self.job.title}"

class CandidateRecommendation(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='candidate_recommendations')
    candidate = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='employer_recommendations')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='candidate_recommendations')
    match_score = models.FloatField()
    is_viewed = models.BooleanField(default=False)
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('employer', 'candidate', 'job')
    
    def __str__(self):
        return f"Candidate recommendation for {self.employer.company_name} - {self.candidate.user.username}"

class RecommendationFeedback(models.Model):
    FEEDBACK_TYPE_CHOICES = (
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
        ('maybe', 'Maybe'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_feedback')
    job_recommendation = models.ForeignKey(JobRecommendation, on_delete=models.CASCADE, null=True, blank=True, related_name='feedback')
    candidate_recommendation = models.ForeignKey(CandidateRecommendation, on_delete=models.CASCADE, null=True, blank=True, related_name='feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.user.username} on recommendation {self.id}"
