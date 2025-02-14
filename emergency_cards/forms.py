from django import forms
from .models import EmergencyCard
import re

class EmergencyCardForm(forms.ModelForm):
    class Meta:
        model = EmergencyCard
        fields = [
            'language',
            'condition',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'custom_message'
        ]
        widgets = {
            'emergency_contact_relationship': forms.TextInput(attrs={
                'placeholder': 'e.g, Parent, Spouse, Siblings'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'placeholder': 'e.g., +1 (555) 123-4567'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'placeholder': 'Full name of emergency contact'
            }),
            'custom_message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'e.g., "Add any specific instructions or notes...'
            }),
        }
    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data['emergency_contact_phone']

        has_plus = phone.startswith('+')
        # remove all non digits
        phone = re.sub(r'\D', '', phone)
        # add country code if needed
        if has_plus:
            phone = f'+1{phone}'
        elif not has_plus:
            phone = f'+1{phone}'

        # check if it's valid phone number format
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone):
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone


    def clean(self):
        cleaned_data = super().clean()
        emergency_contact_name = cleaned_data.get('emergency_contact_name')
        emergency_contact_phone = cleaned_data.get('emergency_contact_phone')
        emergency_contact_relationship = cleaned_data.get('emergency_contact_relationship')

        # Both name and phone are required
        if not emergency_contact_name and not emergency_contact_phone:
            raise forms.ValidationError('You must provide either an emergency contact name or phone number.')

        # Relationship is required if name is provided
        if emergency_contact_name and not emergency_contact_relationship:
            raise forms.ValidationError('Please specify the relationship with the emergency contact.')

         # name should be reasonable length
        if emergency_contact_name and len(emergency_contact_phone) < 2:
            raise forms.ValidationError('Emergency contact name is too short.')

        return cleaned_data
