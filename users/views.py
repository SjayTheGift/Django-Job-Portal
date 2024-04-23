from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views

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
                    messages.error(request, f"{field}: {error}")
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.POST)
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # print(f'email {email} password {password}')

        print(form.is_valid())
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
           
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the desired URL name for the home page
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
