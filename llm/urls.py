from django.urls import path
from llm import views
urlpatterns = [
    
  path('send_message/<int:chat_id>/',views.send_message, name='home'),
]
