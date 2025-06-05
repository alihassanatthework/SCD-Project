
from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.JobCategoryListView.as_view(), name='job_categories'),
    path('', views.JobPostingListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobPostingDetailView.as_view(), name='job_detail'),
    path('create/', views.JobPostingCreateView.as_view(), name='job_create'),
    path('<int:pk>/update/', views.JobPostingUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobPostingDeleteView.as_view(), name='job_delete'),
    path('my-jobs/', views.EmployerJobsView.as_view(), name='employer_jobs'),
    path('applications/', views.JobApplicationListView.as_view(), name='job_applications'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='job_application_detail'),
    path('apply/', views.JobApplicationCreateView.as_view(), name='job_apply'),
    path('<int:job_id>/wishlist/', views.wishlist_toggle, name='wishlist_toggle'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
]
