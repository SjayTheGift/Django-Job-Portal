# job_listing/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import JobSeeker, Employer

from django.contrib.auth import get_user_model

User = get_user_model()

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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def is_valid(self):
        valid = super().is_valid()  # Call the parent's is_valid() method

        if valid:
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')

            # Perform your custom validation logic here
            if not email or not password:
                self.add_error(None, 'Invalid email or password.')

        return valid
