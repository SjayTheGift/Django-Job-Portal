from django.contrib import admin

from .models import User, Employer, JobSeeker

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(JobSeeker)
