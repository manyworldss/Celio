from django.urls import path
from . import views

app_name = 'emergency_cards'

urlpatterns = [
    path('create/', views.create_card, name='create_card'),
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
]

