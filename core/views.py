# subscription/views.py
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscription

class UpgradeSubscriptionView(views.APIView):
    """View for upgrading to premium subscription (DEMO VERSION)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Demo upgrade - instantly upgrade user to premium
        (In production, this would create a Stripe checkout session)
        """
        # Get or create subscription
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            defaults={'plan': Subscription.FREE, 'status': Subscription.STATUS_ACTIVE}
        )
        
        # Upgrade to premium
        subscription.plan = Subscription.PREMIUM
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        
        return Response({
            'success': True,
            'message': 'Upgraded to premium successfully!',
            'redirect_url': '/dashboard/'  # Or wherever you want to redirect after upgrade
        })

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