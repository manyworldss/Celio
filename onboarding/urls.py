from django.urls import path 
from . import views

app_name = 'onboarding'

urlpatterns = [
    path('tour/', views.start_tour, name='start_tour'),
    path('tour/complete/', views.complete_tour, name='complete_tour'),
    path('prompt/', views.show_tour_prompt, name='show_tour_prompt'), 
]