from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class signupform(UserCreationForm):
    username=forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'placeholder':'Enter your Name'})
    )
    password1=forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})
    )
    password2=forms.CharField(
        label="conf-password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your conform-password'})
    )
    email=forms.EmailField (
        label="email",
        widget=forms.EmailInput(attrs={'placeholder':'Enter your email'})
    )

    class Meta:
        model=User 
        fields=['username','password1','password2','email']



class loginform(AuthenticationForm):
    username=forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'placeholder':'enter your name'})
    )
    password=forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})
    )