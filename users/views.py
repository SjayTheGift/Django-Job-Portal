from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegistrationForm

def register(request):
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
        print('not working')
        form = RegistrationForm()
       
    return render(request, 'register.html', {'form': form})


def login(request):
    return render(request, template_name="login.html")
