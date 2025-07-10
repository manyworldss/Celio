from django.urls import path, include
from . import views

app_name = 'message_cards'

urlpatterns = [
    # Main unified card management view
    path('', views.unified_card_management, name='unified_card_management'),
    
    # Legacy/Alternative routes
    path('create/', views.create_card_or_edit, name='create_card'),  # redirects to unified view
    path('edit/', views.create_card_or_edit, name='edit_card'),  # redirects to unified view 
    path('card/detail/', views.card_detail, name='card_detail'),  # card details view
    path('my-card/', views.unified_card_management, name='my_card'),  # user-friendly alias for unified view
    
    # Fullscreen and specialized views
    path('card/fullscreen/', views.fullscreen_card, name='fullscreen_card'),  # fullscreen view
    path('card/delete/', views.delete_card, name='delete_card'),  # delete the card
    path('card/switch-language/', views.switch_language, name='switch_language'),  # language route
    path('validate-field/', views.validate_field, name='validate_field'),
    path('card/download/', views.download_card, name='download_card'),
    path('card/share/', views.share_card, name='share_card'),
    path('card/preview/', views.preview_card, name='preview_card'),
    path('public-card/<uuid:card_id>/', views.public_card, name='public_card'),
    path('api/subscription/', include('subscription.urls')),
    
    # Theme-related URLs
    path('themes/', views.themes, name='themes'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('apply-theme/<str:theme_name>/', views.apply_theme, name='apply_theme'),
    path('mark-tour-seen/', views.mark_tour_seen, name='mark_tour_seen'),
    path('translate_card/', views.translate_card, name='translate_card'),  # New API endpoint for efficient translation
]
