from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import OnboardingStatus

@receiver(post_save, sender=User)
def create_onboarding_status(sender, instance, created, **kwargs):
    if created:
        OnboardingStatus.objects.create(user=instance)
    instance.onboarding_status.save()



