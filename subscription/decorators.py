from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def premium_required(view_func):
    """ Decorator to restrict access to premium users only """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # For the demo, we grant premium access to everyone
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view