from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('search/', views.search, name="search"),
    path('add/', views.add_job, name="add_job"),
    path('job/<int:pk>/', views.job_details, name="job_details"),
]
