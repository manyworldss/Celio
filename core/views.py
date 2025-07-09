from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .models import EarlyAccessSignup
import json

# Sample demo user data
DEMO_USER = {
    'name': 'Demo User',
    'email': 'demo@example.com',
    'has_card': True,
    'is_premium': True,
    'is_demo': True
}

def home(request):
    """Home view with demo mode enabled"""
    # For now, we'll use the new landing page template
    # The demo functionality will be handled by the emergency_cards app
    return render(request, 'core/landing.html')

def reset_demo(request):
    """Reset the demo to initial state"""
    messages.success(request, 'Demo has been reset to default settings.')
    return redirect('core:home')

@csrf_protect
@require_http_methods(["GET", "POST"])
def early_access(request):
    """Early access signup page for mobile app notifications"""
    if request.method == 'POST':
        try:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Get form data
            email = request.POST.get('email', '').strip().lower()
            name = request.POST.get('name', '').strip()
            wants_updates = request.POST.get('updates') == 'on'
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Validate email
            if not email:
                return JsonResponse({
                    'success': False, 
                    'error': 'Email address is required.'
                })
            
            # Create or update signup
            signup, created = EarlyAccessSignup.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'wants_updates': wants_updates,
                    'ip_address': ip_address,
                    'user_agent': user_agent
                }
            )
            
            if not created:
                # Update existing signup
                signup.name = name or signup.name
                signup.wants_updates = wants_updates
                signup.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Your signup has been updated! We\'ll notify you when the mobile app launches.',
                    'existing': True
                })
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for signing up! We\'ll notify you when the mobile app launches.',
                'existing': False
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'An error occurred. Please try again later.'
            })
    
    return render(request, 'core/early_access.html')

# Update the upgrade_page view
def upgrade_page(request):
    """View for the subscription upgrade page"""
    # Check if user already has premium
    is_premium = False
    if request.user.is_authenticated and hasattr(request.user, 'subscription'):
        is_premium = request.user.subscription.is_premium
    
    # Add a success message if redirected after upgrade
    if request.GET.get('upgraded') == 'true':
        messages.success(request, "Congratulations! Your account has been upgraded to Premium!")
    
    return render(request, 'subscription/upgrade.html', {
        'is_premium': is_premium,
        'demo_mode': True  # Flag to indicate demo mode in template
    })





