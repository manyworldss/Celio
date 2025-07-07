# travel/urls.py
from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.travel_guide_list, name='travel_guide_list'),
    path('<slug:slug>/', views.country_detail, name='country_detail'),
    path('<slug:slug>/card/', views.restaurant_card, name='restaurant_card'),

]