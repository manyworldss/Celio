from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_celiac = models.BooleanField(default=False)
    is_gluten_sensitive = models.BooleanField(default=False)
    other_allergies = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s profile"
  # signal to automatically create/upload UserProfile when User is created/updated

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()



# Create your models here.
