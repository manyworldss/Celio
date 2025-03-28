def subscription_status(request):
    """Add subscription status to template context"""
    # For our demo version, everyone gets premium features
    return {
        'is_premium': True,
        'subscription_plan': 'premium',
        'subscription_status': 'active'
    }