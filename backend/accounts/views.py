
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, JobSeekerProfile, EmployerProfile
from .serializers import (
    UserSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer,
    UserRegistrationSerializer, UserLoginSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    user = request.user
    user_data = UserSerializer(user).data
    
    if user.user_type == 'job_seeker':
        try:
            profile = user.job_seeker_profile
            user_data['profile'] = JobSeekerProfileSerializer(profile).data
        except JobSeekerProfile.DoesNotExist:
            JobSeekerProfile.objects.create(user=user)
            profile = user.job_seeker_profile
            user_data['profile'] = JobSeekerProfileSerializer(profile).data
    elif user.user_type == 'employer':
        try:
            profile = user.employer_profile
            user_data['profile'] = EmployerProfileSerializer(profile).data
        except EmployerProfile.DoesNotExist:
            EmployerProfile.objects.create(user=user, company_name=f"{user.username}'s Company")
            profile = user.employer_profile
            user_data['profile'] = EmployerProfileSerializer(profile).data
    
    return Response(user_data)

class JobSeekerProfileUpdateView(generics.UpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = JobSeekerProfile.objects.get_or_create(user=self.request.user)
        return profile

class EmployerProfileUpdateView(generics.UpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = EmployerProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'company_name': f"{self.request.user.username}'s Company"}
        )
        return profile
