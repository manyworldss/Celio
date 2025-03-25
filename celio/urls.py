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
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('emergency_cards/', include('emergency_cards.urls')), # this will handle all card - related URLs
    path('onboarding/', include('onboarding.urls', namespace='onboarding')),
    path('sage/', include('sage.urls', namespace='sage')),
    path('travel/', include('travel.urls', namespace='travel')),
    path('subscription/', include('subscription.urls', namespace='subscription')), # regular views
    path('api/subscription/', include('subscription.urls', namespace='subscription_api')), # api endpoint
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)