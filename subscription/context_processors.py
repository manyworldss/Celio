
def subscription_status(request):
    """Add subscription status to template context"""
    if request.user.is_authenticated:
        try:
            subscription = request.user.subscription
            return {
                'is_premium': subscription.is_premium,
                'subscription_plan': subscription.plan,
                'subscription_status': subscription.status
            }
        except:
            pass
    
    return {
        'is_premium': False,
        'subscription_plan': 'free',
        'subscription_status': 'active'
    }