from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=50,default='New Chat')
    created_at=models.DateTimeField(auto_now_add=True)


class message(models.Model):
    chat=models.ForeignKey(chat, on_delete=models.CASCADE)
    sender=models.CharField(max_length=15)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)