from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def job_details(request, pk):
    return render(request, 'job_details.html', {pk:pk})

def add_job(request):
    return render(request, 'add_job.html', )
