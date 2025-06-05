
#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job, JobApplication
from accounts.models import Profile

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create sample users if they don't exist
    if not User.objects.filter(username='employer1').exists():
        employer = User.objects.create_user(
            username='employer1',
            email='employer@example.com',
            password='password123',
            first_name='John',
            last_name='Employer'
        )
        Profile.objects.create(
            user=employer,
            user_type='employer',
            company_name='Tech Corp',
            bio='Leading technology company'
        )
        print("Created employer user")
    
    if not User.objects.filter(username='jobseeker1').exists():
        jobseeker = User.objects.create_user(
            username='jobseeker1',
            email='jobseeker@example.com',
            password='password123',
            first_name='Jane',
            last_name='Seeker'
        )
        Profile.objects.create(
            user=jobseeker,
            user_type='job_seeker',
            bio='Experienced software developer'
        )
        print("Created job seeker user")
    
    # Create sample jobs
    employer = User.objects.filter(username='employer1').first()
    if employer and Job.objects.count() < 5:
        jobs_data = [
            {
                'title': 'Senior Frontend Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'job_type': 'full_time',
                'salary_min': 100000,
                'salary_max': 150000,
                'description': 'We are looking for an experienced frontend developer to join our team.',
                'requirements': 'React, TypeScript, 3+ years experience'
            },
            {
                'title': 'Backend Engineer',
                'company': 'Tech Corp',
                'location': 'Remote',
                'job_type': 'full_time',
                'salary_min': 90000,
                'salary_max': 140000,
                'description': 'Join our backend team to build scalable systems.',
                'requirements': 'Python, Django, PostgreSQL, 2+ years experience'
            },
            {
                'title': 'UI/UX Designer',
                'company': 'Design Studio',
                'location': 'New York, NY',
                'job_type': 'contract',
                'salary_min': 70000,
                'salary_max': 100000,
                'description': 'Create beautiful and functional user interfaces.',
                'requirements': 'Figma, Adobe Creative Suite, Portfolio required'
            }
        ]
        
        for job_data in jobs_data:
            Job.objects.create(
                employer=employer,
                **job_data
            )
        print(f"Created {len(jobs_data)} sample jobs")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
