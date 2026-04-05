from django.urls import path
from llm import views
urlpatterns = [
   path('',views.home,name='home'),
]
