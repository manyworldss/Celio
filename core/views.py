from django.shortcuts import render, redirect
from django.contrib import messages

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





