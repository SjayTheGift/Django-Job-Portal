from datetime import datetime
from django.db import models
from users.models import Employer


class JobListing(models.Model):
    class Location(models.TextChoices):
        CAPETOWN = 'Cape Town'
        DURBAN = 'Durban'
        JOHANNESBURG = 'Johannesburg'
        GQEBERHA = 'Gqeberha'
    
    class JobType(models.TextChoices):
        REMOTE = 'Remote'
        HYBRID = 'Hybrid'
        ONSITE = 'Onsite'

    company = models.ForeignKey(Employer, on_delete=models.CASCADE)   
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=50, choices=Location.choices)
    job_type = models.CharField(max_length=50, choices=JobType.choices)
    experience = models.CharField(max_length=20)
    salary = models.CharField(max_length=20)
    date_posted = models.DateTimeField(auto_now_add=datetime.now)
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    