from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='landing'),
    path('reset-demo/', views.reset_demo, name='reset_demo'),
    path('early-access/', views.early_access, name='early_access'),
]