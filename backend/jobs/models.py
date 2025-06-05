
from django.db import models
from accounts.models import User, JobSeekerProfile, EmployerProfile

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Job Categories"
    
    def __str__(self):
        return self.name

class JobPosting(models.Model):
    EMPLOYMENT_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    )
    
    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead/Manager'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField(blank=True)
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='job_postings')
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    location = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    skills_required = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"

class JobWishlist(models.Model):
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='wishlist')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job_seeker', 'job')
    
    def __str__(self):
        return f"{self.job_seeker.user.username} - {self.job.title}"

class CandidateWatchlist(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='watchlist')
    candidate = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='watched_by')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('employer', 'candidate')
    
    def __str__(self):
        return f"{self.employer.company_name} watching {self.candidate.user.username}"
