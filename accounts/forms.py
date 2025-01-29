from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_celiac', 'is_gluten_sensitive', 'other_allergies', 'location')
        widgets = {
            'other_allergies': forms.Textarea(attrs={'rows': 3}),
        }