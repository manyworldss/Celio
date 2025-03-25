from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionDetailView(APIView):
    """View for getting current subscription details"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get the user's current subscription"""
        # Try to get user's subscription or create a free one if it doesn't exist
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            defaults={'plan': Subscription.FREE, 'status': Subscription.STATUS_ACTIVE}
        )
        
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

class UpgradeSubscriptionView(APIView):
    """View for upgrading to premium subscription"""
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
            'redirect_url': '/subscription/upgrade/?upgraded=true'
        })

class CancelSubscriptionView(APIView):
    """View for canceling subscription"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Cancel the user's subscription"""
        try:
            subscription = Subscription.objects.get(user=request.user)
            subscription.status = Subscription.STATUS_CANCELED
            subscription.save()
            
            return Response({
                'success': True,
                'message': 'Subscription canceled successfully'
            })
        except Subscription.DoesNotExist:
            return Response({
                'success': False,
                'message': 'No active subscription found'
            }, status=status.HTTP_404_NOT_FOUND)

class StripeWebhookView(APIView):
    """View for handling Stripe webhooks"""
    permission_classes = []  # No authentication needed for webhooks
    
    def post(self, request):
        """Process Stripe webhook events (placeholder for demo)"""
        # In a real implementation, this would process webhook events from Stripe
        return Response({'status': 'received'}, status=status.HTTP_200_OK)

# Regular Django views
@login_required
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

        

    