from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class EmergencyCard(models.Model):

    # theme choices 
    THEME_CLASSIC = 'classic'
    THEME_MODERN = 'modern'
    THEME_MINIMAL = 'minimal'

    THEME_CHOICES = [
        (THEME_CLASSIC, 'Classic'),
        (THEME_MODERN, 'Modern'),
        (THEME_MINIMAL, 'Minimal'),
    ]


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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')
    condition = models.CharField(max_length=3, choices=SEVERITY_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
   
    # storing languages and translations
    translations = models.JSONField(default=dict)
    # timestamps  # This will store all language versions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # theme selection
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default=THEME_CLASSIC, verbose_name='Theme')

def get_message(self, language='EN'):
    """Get the message in the specified language"""
    return self.translations.get(language, self.translations.get( 'EN',''))

def set_message(self, language, message):
    """Set the message in the specified language"""
    if not self.translations:
        self.translations = {}
    self.translations[language] = message
    self.save()

def __str__(self):
    available_languages = list(self.translations.keys())
    languages_string = ",".join(available_languages) if available_languages else "No languages"
    return f"Emergency card for {self.user.username} ({languages_string})"









