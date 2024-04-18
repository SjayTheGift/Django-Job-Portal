from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('account/login/', views.login, name="login"),
    path('account/register/', views.register, name="register"),
]
