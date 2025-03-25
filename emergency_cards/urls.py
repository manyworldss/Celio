from django.urls import path, include
from . import views

app_name = 'emergency_cards'

urlpatterns = [
    path('create/', views.create_card_or_edit, name='create_card'), # create or edit card
    path('card/detail/', views.card_detail, name='card_detail'), # view card details
    path('card/delete/', views.delete_card, name='delete_card'), # delete the card
    path('card/switch-language/', views.switch_language, name='switch_language'), # new language route
    path('validate-field/', views.validate_field, name='validate_field'),
    path('card/download/', views.download_card, name='download_card'),
    path('card/share/', views.share_card, name='share_card'),
    path('card/preview/', views.preview_card, name='preview_card'),
    path('public-card/<int:card_id>/', views.public_card, name='public_card'),
    path('api/subscription/', include('subscription.urls')),
]
