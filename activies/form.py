from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import users
class CreationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
class usersForm(ModelForm):
    class Meta:
        model = users
        fields = '__all__'
        exclude = ['user','date_created','name']
         

    

    
    