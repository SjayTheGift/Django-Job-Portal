from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateJobForm
from .models import JobListing
from users.models import User, Employer

def index(request):
    return render(request, 'index.html')

def jobs_list_view(request):
    jobs = JobListing.objects.order_by("-date_posted")
    context = {"jobs": jobs}
    return render(request, 'jobs_list.html', context)


def job_details(request, pk):
    return render(request, 'job_details.html', {pk:pk})



@login_required(login_url='login')
def check_login_view(request):
    if not request.user.is_authenticated:
        # Set the 'next' parameter in the login URL to redirect to the 'add_job' URL after successful login
        login_url = reverse('login') + '?next=' + reverse('add_job')
        return redirect(login_url)
    else:
        return redirect('add_job')

@login_required(login_url='login')
def add_job(request):

    if not request.user.is_employer:
        return redirect('access_denied')
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Employer profile not found.")
        return redirect('access_denied')  
     
    if request.method == "POST":
        form = CreateJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = employer

            if request.user.is_employer:
                job.save()
                messages.info(request, "New Job has been created")
                return redirect("add_job")
            else:
                messages.warning(request, "User can not add on page")
        else:
            messages.warning(request, "Something went wrong")
    else:
        form = CreateJobForm()
    return render(request, 'add_job.html', {'form': form, 'employer': employer})


