from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'job-seekers', views.JobSeekerViewSet, basename='job-seeker')
router.register(r'employers', views.EmployerViewSet, basename='employer')
router.register(r'feedback', views.UserFeedbackViewSet, basename='feedback')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
] + router.urls 