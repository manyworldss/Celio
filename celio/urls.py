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


urlpatterns = [
    path('admin/', admin.site.urls),  # Keep admin for demo management
    path('', include('core.urls')),  # Main demo landing page
    path('m_cards/', include('message_cards.urls', namespace='message_cards')),  # Card functionality
    path('accounts/', include('accounts.urls')),  # User authentication
    # path('travel/', include('travel.urls', namespace='travel')),  # Travel guides enabled
    path('sage/', include('sage.urls', namespace='sage')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)