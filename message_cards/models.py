from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from .constants import PREDEFINED_MESSAGES, MEDICAL_INFO_BULLETS

class EmergencyCard(models.Model):
    # Theme choices - simplified to 3 essential themes
    THEME_DARK = 'dark'
    THEME_LIGHT = 'light'
    THEME_DARK_PURPLE = 'dark-purple'

    THEME_CHOICES = [
        (THEME_LIGHT, 'Light'),
        (THEME_DARK, 'Dark'),
        (THEME_DARK_PURPLE, 'Dark Purple'),
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

    # Demo card identifier
    card_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=3, choices=SEVERITY_CHOICES, default='CEL', 
                                 verbose_name='Condition', 
                                 help_text='Select the option that best describes your dietary restriction')
    
    # Contact information
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True,
                                             verbose_name='Contact Name',
                                             help_text='Person to contact if needed')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True,
                                              verbose_name='Contact Phone',
                                              help_text='Include country code if traveling internationally (e.g., +1 555-123-4567).')
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True,
                                                     verbose_name='Contact Relationship')
    
    # Additional medical information
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=10, blank=True)
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Custom note for personalization (will be added to predefined message)
    custom_note = models.TextField(blank=True, 
                                  verbose_name='Personal Note',
                                  help_text='Optional: Add a personal note to your card')
    
    # Display options and customization
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en',
                                         verbose_name='Preferred Language',
                                         help_text='The primary language for your card interface')
    profile_picture = models.ImageField(upload_to='message_cards/', null=True, blank=True)
    show_profile_pic = models.BooleanField(default=True, verbose_name='Show Profile Picture')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default=THEME_LIGHT)
    
    # Translations for multiple languages (for custom notes)
    translations = models.JSONField(default=dict, blank=True,
                                   verbose_name='Translations',
                                   help_text='Stores translations of the custom note')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to get the message in the selected language
    def get_message(self, language_code='en'):
        """
        Get the full message for this card in the specified language,
        combining the predefined condition-specific message with any custom note.
        """
        # Convert language code to lowercase to match our constants structure
        language_code = language_code.lower()
        
        # Get the predefined message for this condition and language
        # Default to English if the requested language isn't available
        predefined_msg = PREDEFINED_MESSAGES.get(self.condition, {}).get(
            language_code, 
            PREDEFINED_MESSAGES.get(self.condition, {}).get('en', '')
        )
        
        # If there's a custom note, add it to the predefined message
        custom_note = self.get_custom_note(language_code)
        if custom_note:
            # Add a line break between the predefined message and custom note
            return f"{predefined_msg}\n\n{custom_note}"
        
        return predefined_msg

    def get_custom_note(self, language_code='en'):
        """
        Get the custom note in the specified language if available,
        otherwise return the custom note in the primary language.
        """
        language_code = language_code.lower()
        
        # If no custom note or translations, return empty string
        if not self.custom_note and not self.translations:
            return ""
        
        # If custom note exists but no translations yet, return the primary custom note
        if self.custom_note and not self.translations:
            return self.custom_note
        
        # Try to get translated custom note from translations
        if language_code in self.translations:
            return self.translations[language_code]
        
        # If no translation for this language, use primary language note
        return self.custom_note
    
    def set_custom_note(self, language_code, note_text):
        """
        Set or update the custom note for a specific language
        """
        language_code = language_code.lower()
        
        # If this is the primary language, update the main custom_note field
        if language_code == self.preferred_language.lower():
            self.custom_note = note_text
        
        # Always update the translations dictionary
        if not self.translations:
            self.translations = {}
        
        # Store in translations dictionary
        self.translations[language_code] = note_text
        
    def get_medical_info_bullets(self, language_code='en'):
        """
        Get the medical information bullet points for the selected condition and language
        """
        language_code = language_code.lower()
        
        # Get bullet points for this condition and language, default to English if not available
        return MEDICAL_INFO_BULLETS.get(self.condition, {}).get(
            language_code, 
            MEDICAL_INFO_BULLETS.get(self.condition, {}).get('en', [])
        )

    def get_theme_choices(self):
        """Return the theme choices for the dropdown"""
        return self.THEME_CHOICES
    


    def __str__(self):
        display_name = self.user_name or "Demo"
        return f"{display_name}'s Card"
        
    @property
    def purpose_text(self):
        """Returns a text description of the card's purpose based on condition"""
        condition_mapping = {
            'CEL': 'Celiac Disease Card',
            'SEN': 'Gluten Sensitivity Alert Card',
            'ALL': 'Wheat/Gluten Allergy Alert Card'
        }
        return condition_mapping.get(self.condition, 'Medical Alert Card')
