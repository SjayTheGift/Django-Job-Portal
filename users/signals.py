from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Employer, JobSeeker

@receiver(post_save, sender=User)
def create_employer_or_jobseeker(sender, instance, created, **kwargs):
    if created:
        if instance.is_job_seeker:
            JobSeeker.objects.create(user=instance)
            instance.jobseeker.save()
        if instance.is_employer:
            Employer.objects.create(user=instance)
            instance.employer.save()
