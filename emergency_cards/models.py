from django.db import models
from django.contrib.auth.models import User

class EmergencyCard(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('ES', 'Spanish'),
        ('FR','French'),
        ('ZH', 'Chinese'),
        ('JA', 'Japanese'),
        ('PT', 'Portuguese'),
         ]
    SEVERITY_CHOICES = [
        ('CEL', 'Celiac Disease'),
        ('SEN', 'Gluten Sensitive'),
        ('ALL', 'Wheat/Gluten Allergy'),
    ]

        # core fields

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    condition = models.CharField(
        max_length=3,
        choices= SEVERITY_CHOICES,
        help_text="Select your gluten-related condition"
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='EN'
    )

    # emergency contact information
emergency_contact_name = models.CharField(max_length=100)
emergency_contact_phone = models.CharField(max_length=20)
emergency_contact_relationship = models.CharField(max_length=50)
    # custom message (optional)
customer_message = models.TextField(
    blank=True, # makes this an optional choice
    help_text="Add any specific instructions or notes regarding your condition",
    max_length=200,
)

# time stamps
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.get_language_display()} card for {self.user.username}"









