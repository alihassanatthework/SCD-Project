
from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobRecommendationListView.as_view(), name='job_recommendations'),
]
