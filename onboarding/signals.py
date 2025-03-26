from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import OnboardingStatus

@receiver(post_save, sender=User)
def create_onboarding_status(sender, instance, created, **kwargs):
    """Create or update onboarding status when a user is created or saved"""
    if created:
        OnboardingStatus.objects.create(user=instance)
    else:
        # Only try to save if the onboarding status already exists
        try:
            if hasattr(instance, 'onboarding_status'):
                instance.onboarding_status.save()
        except OnboardingStatus.DoesNotExist:
            # If it doesn't exist for some reason, create it
            OnboardingStatus.objects.create(user=instance)
