from django.utils import translation
from django.conf import settings

class DefaultLanguageMiddleware:
    """
    Middleware to ensure the default language is always set to English
    unless explicitly changed by the user in the app.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if language is explicitly set in the session or URL
        if not (request.GET.get('lang') or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)):
            # Force English as default language
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        
        response = self.get_response(request)
        return response
