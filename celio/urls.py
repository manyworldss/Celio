"""
URL configuration for celio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, Http404
from django.views.static import serve
import os

def custom_media_serve(request, path):
    """Custom media file serving with proper headers and range support for video files"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if not os.path.exists(file_path):
            raise Http404("Media file not found")
        
        # Get file info
        file_size = os.path.getsize(file_path)
        
        # Handle range requests for video streaming
        range_header = request.META.get('HTTP_RANGE')
        if range_header and path.endswith(('.mp4', '.webm', '.ogg')):
            # Parse range header
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1
            
            # Ensure valid range
            start = max(0, start)
            end = min(file_size - 1, end)
            content_length = end - start + 1
            
            # Read the requested range
            with open(file_path, 'rb') as f:
                f.seek(start)
                data = f.read(content_length)
                
            response = HttpResponse(data, status=206)  # Partial Content
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Content-Length'] = content_length
        else:
            # Serve full file
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read())
            response['Content-Length'] = file_size
            
        # Set appropriate headers for video files
        if path.endswith(('.mp4', '.webm', '.ogg')):
            response['Content-Type'] = 'video/mp4' if path.endswith('.mp4') else 'video/webm'
            response['Accept-Ranges'] = 'bytes'
            response['Cache-Control'] = 'public, max-age=3600'
            
        return response
        
    except Exception as e:
        raise Http404(f"Error serving media file: {str(e)}")

urlpatterns = [
    path('admin/', admin.site.urls),  # Keep admin for demo management
    path('', include('core.urls')),  # Main demo landing page
    path('m_cards/', include('message_cards.urls', namespace='message_cards')),  # Card functionality
    path('accounts/', include('accounts.urls')),  # User authentication
    path('travel/', include('travel.urls', namespace='travel')),
    path('sage/', include('sage.urls', namespace='sage')),
    path('media/<path:path>', custom_media_serve, name='media'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)