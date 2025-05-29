from django.contrib import admin
from .models import JobRecommendation, CandidateRecommendation, RecommendationFeedback

@admin.register(JobRecommendation)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'match_score', 'is_viewed', 'is_applied', 'created_at')
    list_filter = ('is_viewed', 'is_applied', 'created_at')
    search_fields = ('job_seeker__user__email', 'job__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CandidateRecommendation)
class CandidateRecommendationAdmin(admin.ModelAdmin):
    list_display = ('employer', 'candidate', 'job', 'match_score', 'is_viewed', 'is_contacted', 'created_at')
    list_filter = ('is_viewed', 'is_contacted', 'created_at')
    search_fields = ('employer__company_name', 'candidate__user__email', 'job__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'created_at')
    list_filter = ('feedback_type', 'created_at')
    search_fields = ('user__email', 'comments')
    readonly_fields = ('created_at',)
