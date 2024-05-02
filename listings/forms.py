from django import forms
from .models import JobListing

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ('title', 'description', 'location', 'job_type', 'experience', 'salary')