from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse

from .forms import RegistrationForm, LoginForm

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
                return redirect(get_success_url(request))
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