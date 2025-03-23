from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def premium_required(view_func):
    """ Decorator to restrict access to premium users only """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # check if user has premium sub 
        has_premium = False 

        if hasattr(request.user, 'subscription'):
            has_premium = request.user.subscription.is_premium
        
        if has_premium:
            return view_func(request, *args, **kwargs)
        
        else:# redirect to upgrade page
            messages.info(request, 'You need a premium subscription to access this feature.')
            return redirect(reverse('subscription:upgrade'))
    
    return _wrapped_view
    