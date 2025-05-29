from django.contrib import admin
from .models import JobCategory, JobPosting, JobApplication, JobWishlist, CandidateWatchlist

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'category', 'employment_type', 'location', 'is_active', 'created_at')
    list_filter = ('employment_type', 'experience_level', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'employer__company_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'applicant__user__email', 'cover_letter')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobWishlist)
class JobWishlistAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job_seeker__user__email', 'job__title')

@admin.register(CandidateWatchlist)
class CandidateWatchlistAdmin(admin.ModelAdmin):
    list_display = ('employer', 'candidate', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('employer__company_name', 'candidate__user__email', 'notes')
