from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class EmergencyCard(models.Model):
    # Theme choices - simplified to 3 essential themes
    THEME_DARK = 'dark'
    THEME_MEDICAL = 'medical'
    THEME_MINIMAL = 'minimal'

    THEME_CHOICES = [
        (THEME_DARK, 'Dark Theme'),
        (THEME_MEDICAL, 'Medical Theme'),
        (THEME_MINIMAL, 'Minimal Theme'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ja', 'Japanese'),
        ('zh', 'Chinese'),
    ]
    
    SEVERITY_CHOICES = [
        ('CEL', 'Celiac Disease'),
        ('SEN', 'Gluten Sensitive'),
        ('ALL', 'Wheat/Gluten Allergy'),
    ]

    # User and basic information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=3, choices=SEVERITY_CHOICES, default='CEL', 
                                 verbose_name='Condition', 
                                 help_text='Select the option that best describes your dietary restriction')
    
    # Emergency contact information
    emergency_contact_name = models.CharField(max_length=100, blank=True, 
                                             verbose_name='Emergency Contact Name',
                                             help_text='Person to contact in case of an emergency')
    emergency_contact_phone = models.CharField(max_length=20, blank=True,
                                              verbose_name='Emergency Contact Phone',
                                              help_text='Include country code if traveling internationally (e.g., +1 555-123-4567).')
    emergency_contact_relationship = models.CharField(max_length=50, blank=True,
                                                     verbose_name='Emergency Contact Relationship')
    
    # Additional medical information
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=10, blank=True)
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Display options and customization
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en',
                                         verbose_name='Preferred Language',
                                         help_text='The primary language for your card interface')
    profile_picture = models.ImageField(upload_to='emergency_cards/', null=True, blank=True)
    show_profile_pic = models.BooleanField(default=True, verbose_name='Show Profile Picture')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default=THEME_MINIMAL)
    
    # Translations for multiple languages
    translations = models.JSONField(default=dict, blank=True,
                                   verbose_name='Translations',
                                   help_text='Stores the card content in multiple languages')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to get the message in the selected language
    def get_message(self, language_code='EN'):
        """Get the message for this card in the specified language"""
        # Default to English or first available language if the requested one doesn't exist
        if not self.translations:
            return "No information provided yet."
        
        language_code = language_code.upper()
        if language_code in self.translations:
            return self.translations[language_code]
        elif 'EN' in self.translations:
            return self.translations['EN']
        else:
            # Return the first available language if nothing else works
            return next(iter(self.translations.values()))

    def get_message_for_language(self, language_code=None):
        """Get the message for a specific language"""
        if not language_code:
            language_code = self.preferred_language.upper()
        return self.get_message(language_code)

    def get_theme_choices(self):
        """Return the theme choices for the dropdown"""
        return self.THEME_CHOICES
    
    def set_message(self, language, message):
        """Set the message in the specified language"""
        if not self.translations:
            self.translations = {}
        self.translations[language] = message
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Emergency Card"
        
    @property
    def purpose_text(self):
        """Returns a text description of the card's purpose based on condition"""
        condition_mapping = {
            'CEL': 'Celiac Disease Emergency Card',
            'SEN': 'Gluten Sensitivity Alert Card',
            'ALL': 'Wheat/Gluten Allergy Alert Card'
        }
        return condition_mapping.get(self.condition, 'Medical Alert Card')
