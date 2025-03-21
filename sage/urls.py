# sage/urls.py
from django.urls import path
from . import views

app_name = 'sage'

urlpatterns = [
    path('', views.sage_assistant, name='assistant'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]

