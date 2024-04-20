# job_listing/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User, JobSeeker, Employer

class RegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('employer', 'Employer'),
        ('jobseeker', 'Job Seeker'),
    )
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPES)

    class Meta:
            model = User
            fields = ('email', 'password1', 'password2', 'user_type')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            user_type = self.cleaned_data.get('user_type')
            if user_type == 'employer':
                group = Group.objects.get(name='Employers')
                Employer.objects.create(user=user)
            elif user_type == 'jobseeker':
                group = Group.objects.get(name='Job Seekers')
                JobSeeker.objects.create(user=user)
            user.groups.add(group)

        return user

    