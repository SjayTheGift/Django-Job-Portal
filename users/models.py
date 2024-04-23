from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    is_job_seeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    company_description = models.TextField()

    def __str__(self) -> str:
        return self.user.email


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    education_history = models.TextField()
    desired_roles = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.email