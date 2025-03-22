# travel/urls.py
from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.travel_guide_list, name='travel_guide_list'),
    path('<str:country_code>/', views.country_detail, name='country_detail'),
    path('<str:country_code>/card/', views.restaurant_card, name='restaurant_card'),
]