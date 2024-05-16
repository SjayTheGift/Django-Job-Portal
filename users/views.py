from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse

from .forms import RegistrationForm, LoginForm
from .models import Employer, User, JobSeeker

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            if user_type == 'jobseeker':
                user.is_job_seeker = True
            else:
                user.is_employer = True
            user.save()
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
           
            if user is not None:
                login(request, user)
                if request.user.is_job_seeker:
                    return redirect('job_seeker_profile')
                else:
                    return redirect('employer_profile')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') 


def get_success_url(request):
    next_url = request.POST.get('next')
    print(next_url)

    if next_url and next_url != '':
        return next_url
    else:
        return reverse('add_job')


@login_required(login_url='login')
def employer_profile_view(request):
    if not request.user.is_authenticated or not request.user.is_employer:
        return redirect('access_denied')
    
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        employer = None
    
    if request.method == "POST":
        # Handle the form submission and update the profile
        # Assuming the form fields are named 'company_name', 'industry', 'contact_info', and 'company_description'
        company_name = request.POST.get('company_name')
        industry = request.POST.get('industry')
        contact_info = request.POST.get('contact_info')
        company_description = request.POST.get('company_description')

        if employer:
            # Update the existing employer profile
            employer.company_name = company_name
            employer.industry = industry
            employer.contact_info = contact_info
            employer.company_description = company_description
            employer.company_info_done = True
            employer.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('employer_profile')  # Replace 'employer_profile_view' with the appropriate URL or view name
    
    context = {
        'employer': employer
    }
    
    return render(request, 'employer_profile.html', context)

@login_required(login_url='login')
def job_seeker_profile_view(request):
    if not request.user.is_authenticated or not request.user.is_job_seeker:
        return redirect('access_denied')
    
    try:
        job_seeker = JobSeeker.objects.get(user=request.user)
    except Employer.DoesNotExist:
        job_seeker = None
    
    if request.method == "POST":
        # Handle the form submission and update the profile
        # Assuming the form fields are named 'company_name', 'industry', 'contact_info', and 'company_description'
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        education_history = request.POST.get('education_history')
        desired_roles = request.POST.get('desired_roles')

        if job_seeker:
            # Update the existing employer profile
            job_seeker.first_name = first_name
            job_seeker.last_name = last_name
            job_seeker.education_history = education_history
            job_seeker.desired_roles = desired_roles
            job_seeker.job_seeker_profile_done = True
            job_seeker.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('job_seeker_profile')  # Replace 'employer_profile_view' with the appropriate URL or view name
    
    context = {
        'job_seeker': job_seeker
    }
    
    return render(request, 'job_seeker_profile.html', context)