# from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .forms import DatabaseUserCreationForm, DatabaseUserChangeForm
from .models import DatabaseUser
from django.shortcuts import get_object_or_404

# from django.contrib.auth.forms import UserCreationForm
# from django import forms

class SignUp(generic.CreateView):
    form_class = DatabaseUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# https://stackoverflow.com/a/21122537/3211506
class UpdateUser(generic.edit.UpdateView):
    form_class = DatabaseUserChangeForm
    # https://stackoverflow.com/a/23155078/3211506
    # model = DatabaseUser
    def get_object(self):
        return get_object_or_404(DatabaseUser, pk=self.request.user.id)
    success_url = reverse_lazy('home')
    template_name = 'registration/updateUser.html'
