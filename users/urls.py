from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('employer/profile/', views.employer_profile_view, name='employer_profile'),
    path('jobseeker/profile/', views.job_seeker_profile_view, name='job_seeker_profile'),
]
