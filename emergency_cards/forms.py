from django import forms
from .models import EmergencyCard

class EmergencyCards(forms.ModelForm):
    class Meta:
        model = EmergencyCard
        fields = [
            'language',
            'condition',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'customer_message'
        ]
        widgets = {
            'customer_message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add any specific instructions or notes...'}),
            'emergency_contact_phone': forms.Textarea(attrs={'placeholder':'e.g., +1 (555) 123-4567'})
        }