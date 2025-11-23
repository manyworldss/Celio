from django import forms
from .models import EmergencyCard
import re


class EmergencyCardForm(forms.ModelForm):
    """Form for creating and editing message cards in demo mode without user accounts."""

    message_en = forms.CharField(widget=forms.Textarea, required=False, label="Message (English)")
    message_es = forms.CharField(widget=forms.Textarea, required=False, label="Message (Spanish)")
    message_fr = forms.CharField(widget=forms.Textarea, required=False, label="Message (French)")
    message_zh = forms.CharField(widget=forms.Textarea, required=False, label="Message (Chinese)")
    message_ja = forms.CharField(widget=forms.Textarea, required=False, label="Message (Japanese)")
    message_pt = forms.CharField(widget=forms.Textarea, required=False, label="Message (Portuguese)")

    class Meta:
        model = EmergencyCard
        fields = [
            'user_name',
            'condition',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'profile_picture',
            'show_profile_pic',
            'theme',
            'preferred_language',
        ]
        help_texts = {
            'user_name': 'Your name as it should appear on the card',
            'condition': 'Select the condition that best describes your dietary restriction',
        }
        widgets = {
            'emergency_contact_relationship': forms.TextInput(attrs={
                'placeholder': 'e.g., Spouse, Parent, Friend'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'placeholder': '+1 555-123-4567'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'placeholder': 'Full name of contact'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'block w-full rounded-lg border border-gray-300 px-4 py-3 focus:ring-purple-500 focus:border-purple-500'
        
        # If we have an instance (editing an existing card), populate language fields
        if self.instance and self.instance.pk:
            for lang_code, lang_name in EmergencyCard.LANGUAGE_CHOICES:
                field_name = f'message_{lang_code.lower()}'
                if hasattr(self, field_name) and lang_code in self.instance.translations:
                    self.initial[field_name] = self.instance.translations[lang_code]

    def save(self, commit=True):
        instance = super().save(commit=False)
        translations = {}
        
        # Extract and save all language messages
        for lang_code, lang_name in EmergencyCard.LANGUAGE_CHOICES:
            field_name = f'message_{lang_code.lower()}'
            if hasattr(self, 'cleaned_data') and field_name in self.cleaned_data and self.cleaned_data[field_name]:
                translations[lang_code] = self.cleaned_data[field_name]
        
        # Always ensure at least one language is present
        # If no languages were provided, use English with a default message
        if not translations:
            translations['EN'] = "I have celiac disease/gluten sensitivity and cannot consume any foods containing gluten."
        # If English wasn't provided but another language was, copy that to English
        elif 'EN' not in translations and translations:
            # Use the first available language as English fallback
            first_lang = next(iter(translations))
            translations['EN'] = translations[first_lang]
            
        instance.translations = translations
        
        if commit:
            instance.save()
            
        return instance

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data['emergency_contact_phone']

        # Check if phone is empty and return as is (other validation will catch if required)
        if not phone:
            return phone

        has_plus = phone.startswith('+')
        # remove all non digits
        digits_only = re.sub(r'\D', '', phone)
        
        # add country code if needed
        if has_plus:
            formatted_phone = f'+{digits_only}'
        else:
            # Add default country code +1 if not present
            formatted_phone = f'+1{digits_only}'

        # check if it's valid phone number format (at least 10 digits after potential +)
        phone_pattern = re.compile(r'^\+\d{10,15}$')
        if not phone_pattern.match(formatted_phone):
            raise forms.ValidationError('Please enter a valid phone number with at least 10 digits.')
        return formatted_phone

    def clean(self):
        cleaned_data = super().clean()
        emergency_contact_name = cleaned_data.get('emergency_contact_name')
        emergency_contact_phone = cleaned_data.get('emergency_contact_phone')
        emergency_contact_relationship = cleaned_data.get('emergency_contact_relationship')

        # Relaxed validation for demo mode
        # if not emergency_contact_name and not emergency_contact_phone:
        #     raise forms.ValidationError('You must provide either a contact name or phone number.')

        # If name is provided, relationship should also be provided
        if emergency_contact_name and not emergency_contact_relationship:
            raise forms.ValidationError('Please specify the relationship with the contact.')

        # Validate name length
        if emergency_contact_name and len(emergency_contact_name) < 2:
            raise forms.ValidationError('Contact name is too short.')

        return cleaned_data


class SimpleEmergencyCardForm(forms.ModelForm):
    """Simplified form for the E-Card view with only essential fields."""
    class Meta:
        model = EmergencyCard
        fields = [
            'user_name',
            'condition',
            'custom_note',
            'theme',
            'preferred_language',
        ]
        widgets = {
            'custom_note': forms.Textarea(attrs={'rows': 4}),
        }