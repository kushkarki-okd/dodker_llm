from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class signupform(UserCreationForm):
    Name=forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'placeholder':'Enter your Name'})
    )
    password=forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})
    )
    conf_password=forms.CharField(
        label="conf-password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your conform-password'})
    )
    Email=forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder':'Enter your email'})
    )

    class Meta:
        model=User 
        fields=['Name','password','conf_password','Email']



class loginform(AuthenticationForm):
    Name=forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'placeholder':'enter your name'})
    )
    password=forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})
    )