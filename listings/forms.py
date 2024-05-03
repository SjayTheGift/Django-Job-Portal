from django import forms
from .models import JobListing

class CreateJobForm(forms.ModelForm):

    class Meta:
        model = JobListing
        fields = ('title', 'description', 'location', 'job_type', 'experience', 'salary')
        exclude = ['company']  # Exclude the 'company' field from the form

    
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)  # Retrieve the 'company' argument
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.company:
            instance.company = self.company
        if commit:
            instance.save()
        return instance