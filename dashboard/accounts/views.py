# from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .forms import DatabaseUserCreationForm
from .models import DatabaseUser

# from django.contrib.auth.forms import UserCreationForm
# from django import forms

class SignUp(generic.CreateView):
    form_class = DatabaseUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
