from django.urls import path
from llm import views
urlpatterns = [
    path('',views.home , name='home'),
    path('chat_page',views.chat_page, name='chat_page'),  
    path('send_message/<int:chat_id>/',views.send_message, name='home'),
    path('create_chat',views.create_chat,name='create_chat')
]
