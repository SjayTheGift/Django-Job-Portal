from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add/', views.add_job, name="add_job"),
    path('update/job/<int:pk>', views.update_job_view, name="update_job"),
    path('jobs/', views.jobs_list_view, name="jobs_list"),
    path('job/<int:pk>/', views.job_details, name="job_details"),
    path('search/', views.search_jobs_view, name='search'),
    path('access-denied/', TemplateView.as_view(template_name='access_denied.html'), name='access_denied'),
]
