from django.db import models
from django.contrib.auth.models import User 


class Subscription(models.Model):
     # main sub tiers 
    FREE = 'free'
    PREMIUM = 'premium'

    SUBSCRIPTION_CHOICES = [
        (FREE, 'Free'),
        (PREMIUM, 'Premium'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_CANCELED = 'canceled'
    STATUS_EXPIRED = 'expired'
    STATUS_TRIAL = 'trial'


    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_TRIAL, 'Trial'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default=FREE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    start_date = models.DateTimeField(auto_now_add=True)    
    end_date = models.DateTimeField(null=True, blank=True)
            
    
    # stripe customer id numbers 
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.get_plan_display()} subscription ({self.get_status_display()})"

    @property
    def is_active(self):
    #Check if the sub is active
        return self.status == self.STATUS_ACTIVE or self.status == self.STATUS_TRIAL
    
    @property
    def is_premium(self):
        # check if user has premium subscription
        return self.is_active and self.plan == self.PREMIUM
    


# Create your models here.
