# Generated by Django 5.0.4 on 2024-05-02 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='company_info_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='job_seeker_profile_done',
            field=models.BooleanField(default=False),
        ),
    ]