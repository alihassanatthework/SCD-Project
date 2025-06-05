
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/job-seeker/', views.JobSeekerProfileUpdateView.as_view(), name='job_seeker_profile_update'),
    path('profile/employer/', views.EmployerProfileUpdateView.as_view(), name='employer_profile_update'),
]
