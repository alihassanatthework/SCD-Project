
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from accounts.models import User, JobSeekerProfile, EmployerProfile
from jobs.models import JobCategory, JobPosting

# Create categories
categories = [
    {'name': 'Software Development', 'description': 'Software engineering and development roles'},
    {'name': 'Data Science', 'description': 'Data analysis and machine learning roles'},
    {'name': 'Design', 'description': 'UI/UX and graphic design roles'},
    {'name': 'Marketing', 'description': 'Digital marketing and content roles'},
    {'name': 'Sales', 'description': 'Sales and business development roles'},
]

for cat_data in categories:
    JobCategory.objects.get_or_create(**cat_data)

# Create sample employer
employer_user = User.objects.create_user(
    username='techcorp',
    email='hr@techcorp.com',
    password='password123',
    user_type='employer',
    first_name='Tech',
    last_name='Corp'
)

employer_profile = EmployerProfile.objects.create(
    user=employer_user,
    company_name='TechCorp Solutions',
    company_description='Leading technology solutions provider',
    company_website='https://techcorp.com',
    industry='Technology',
    location='San Francisco, CA'
)

# Create sample job seeker
jobseeker_user = User.objects.create_user(
    username='johndoe',
    email='john@example.com',
    password='password123',
    user_type='job_seeker',
    first_name='John',
    last_name='Doe'
)

jobseeker_profile = JobSeekerProfile.objects.create(
    user=jobseeker_user,
    bio='Experienced software developer with 5 years of experience',
    skills='Python, JavaScript, React, Django',
    experience_years=5,
    location='San Francisco, CA',
    expected_salary=100000
)

# Create sample jobs
software_category = JobCategory.objects.get(name='Software Development')

jobs = [
    {
        'title': 'Senior Full Stack Developer',
        'description': 'We are looking for a senior full stack developer to join our team.',
        'requirements': 'Bachelor\'s degree in Computer Science, 5+ years experience',
        'responsibilities': 'Develop and maintain web applications, collaborate with team',
        'employment_type': 'full_time',
        'experience_level': 'senior',
        'location': 'San Francisco, CA',
        'salary_min': 120000,
        'salary_max': 180000,
        'skills_required': 'Python, Django, React, PostgreSQL',
        'benefits': 'Health insurance, 401k, flexible hours'
    },
    {
        'title': 'Frontend Developer',
        'description': 'Join our frontend team to build amazing user interfaces.',
        'requirements': 'Experience with React, TypeScript, and modern CSS',
        'responsibilities': 'Build responsive web applications, work with designers',
        'employment_type': 'full_time',
        'experience_level': 'mid',
        'location': 'Remote',
        'salary_min': 80000,
        'salary_max': 120000,
        'skills_required': 'React, TypeScript, CSS, HTML',
        'benefits': 'Remote work, health insurance, learning budget'
    }
]

for job_data in jobs:
    JobPosting.objects.create(
        employer=employer_profile,
        category=software_category,
        **job_data
    )

print("Sample data created successfully!")
