from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer
from serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    """View for getting current sub status"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """try to get users sub or create a free one if it doesnt exist"""
        subscription = Subscription.objects.get_or_create(
            user=request.user,
            defaults={'plan': Subscription.FREE,'status': Subscription.STATUS_ACTIVE
            })
        
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

class UpgradeView(views.APIView):
    """View for upgrading sub"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Handle sub upgrade and implement stripe API"""
        pass

class CancelSubscriptionView(views.APIView):
    """View for canceling sub"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Cancel User Subscription"""
        
        pass

class StripeWebHookView(views.APIView):
    """View for handling stripe webhooks"""
    permission_classes = []  # no auth required for webhooks

    def post(self, request):
        """Handle Stripe Webhook implement various webhook events"""
        pass
# subscription/views.py (add this function)
def upgrade_page(request):
    """View for the subscription upgrade page"""
    # Check if user already has premium
    is_premium = False
    if request.user.is_authenticated and hasattr(request.user, 'subscription'):
        is_premium = request.user.subscription.is_premium
    
    return render(request, 'subscription/upgrade.html', {
        'is_premium': is_premium
    })

# subscription/urls.py (add this URL)
path('upgrade/', views.upgrade_page, name='upgrade_page'),

        

    