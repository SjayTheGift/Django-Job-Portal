from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateJobForm, UpdateJobForm
from .models import JobListing
from users.models import User, Employer

def index(request):
    jobs = JobListing.objects.order_by("-date_posted")[:3]
    context = {"jobs": jobs}
    return render(request, 'index.html', context)

def jobs_list_view(request):
    jobs = JobListing.objects.order_by("-date_posted")
    context = {"jobs": jobs}
    return render(request, 'jobs_list.html', context)


def job_details(request, pk):
    job = get_object_or_404(JobListing, id=pk)
    employer = Employer.objects.get(user=job.company.user)
    
    can_edit = job.company.user == request.user
    context = {"job": job, "can_edit": can_edit, "employer": employer}
    return render(request, 'job_details.html', context)



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
                messages.success(request, "New Job has been created")
                return redirect("add_job")
            else:
                messages.warning(request, "User can not add on page")
        else:
            messages.warning(request, "Something went wrong")
    else:
        form = CreateJobForm()
    return render(request, 'add_job.html', {'form': form, 'employer': employer})

@login_required(login_url='login')
def update_job_view(request, pk):
    job = get_object_or_404(JobListing, id=pk)

    if job.company.user != request.user:
        return redirect('access_denied')
    
    if not request.user.is_employer:
        return redirect('access_denied')
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Employer profile not found.")
        return redirect('access_denied')  

    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job, company=request.user)
        if form.is_valid():
            form.save()
            if request.user.is_employer:
                messages.success(request, "Job has been updated")
                return redirect(reverse('update_job', kwargs={'pk': pk})) 
            else:
                messages.warning(request, "User can not update on page")
        else:
            messages.warning(request, "Something went wrong")
    else:
        form = UpdateJobForm(instance=job, company=request.user)
    
    context = {
        'form': form,
        'job': job,
        "employer": employer,
    }
    
    return render(request, 'update_job.html', context)


def search_jobs_view(request):
    query = request.GET.get('title', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')

    jobs = JobListing.objects.all().order_by("-date_posted")

    if query:
        jobs = jobs.filter(title__icontains=query)

    if location:
        jobs = jobs.filter(location__iexact=location)

    if job_type:
        jobs = jobs.filter(job_type__iexact=job_type)

    filtered_jobs = jobs

    context = {
        'jobs': filtered_jobs,
        'query': query,
        'location': location,
        'job_type': job_type,
    }

    return render(request, 'search.html', context)