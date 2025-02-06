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
    # Medical Info (gluten related) >>>
is_celiac = models.BooleanField(default=False)
is_gluten_sensitive = models.BooleanField(default=False)
has_wheat_allergy = models.BooleanField(default=False)
    # Additional medical info >>>
additional_allergies = models.TextField(
    blank=True,
    help_text="List any additional allergies or medical conditions")
    # emergency contact info >>>
emergency_contact_name = models.CharField(
    max_length=100,
    help_text= "Name of Emergency Contact"
)
emergency_contact_phone = models.CharField(
    max_length=20,
    help_text= "Emergency contact phone number"
)
emergency_contact_relationship = models.CharField(
    max_length=50,
    help_text="Relationship of emergency contact (e.g. Parent, Spouse, Sibling)"
)







