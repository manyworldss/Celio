from django.db import models
from django.contrib.auth.models import User

class OnboardingStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding_status')
    has_completed_tour = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding Status for {self.user.username}"


# Create your models here.
