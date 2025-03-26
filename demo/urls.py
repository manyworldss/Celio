from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('start/', views.start_demo, name='start'),
    path('end/', views.end_demo, name='end'),
    path('end_tour/', views.end_tour, name='end_tour'),
]
