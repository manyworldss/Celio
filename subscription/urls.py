from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('', views.SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('upgrade/', views.UpgradeSubscriptionView.as_view(), name='upgrade'),
    path('cancel/', views.CancelSubscriptionView.as_view(), name='cancel'),
    path('webhook/', views.StripeWebhookView.as_view(), name='webhook'),
    # Regular Django view for the upgrade page
    path('upgrade-page/', views.upgrade_page, name='upgrade_page'),
]