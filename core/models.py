from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator

class EarlyAccessSignup(models.Model):
    """Model to store early access email signups securely"""
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Email address for mobile app notifications"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional name of the user"
    )
    wants_updates = models.BooleanField(
        default=False,
        help_text="Whether user wants development updates"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the signup was created"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address for security tracking"
    )
    user_agent = models.TextField(
        blank=True,
        help_text="Browser user agent for security"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether email has been verified"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Early Access Signup"
        verbose_name_plural = "Early Access Signups"
    
    def __str__(self):
        return f"{self.email} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def display_name(self):
        """Return name if provided, otherwise email prefix"""
        if self.name:
            return self.name
        return self.email.split('@')[0]
