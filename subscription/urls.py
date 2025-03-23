from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('', views.SubscriptionViewSet.as_view(), name='subscription'),
    path('upgrade/', views.UpgradeView.as_view(), name='upgrade'),
    path('cancel/', views.CancelSubscriptionView.as_view(), name='cancel'),
    path('webhook/', views.StripeWebHookView.as_view(), name='webhook'),
]
