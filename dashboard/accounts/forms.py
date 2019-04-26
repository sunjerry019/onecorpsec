from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import DatabaseUser

class DatabaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = DatabaseUser
        fields = ('username', 'email', 'reply_to', 'name', 'sign_off_name' )

class DatabaseUserChangeForm(UserChangeForm):
    class Meta:
        model = DatabaseUser
        fields = ('username', 'email', 'name', 'sign_off_name')
