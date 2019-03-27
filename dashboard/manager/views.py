from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.template import RequestContext
from .models import getTable


class Home(generic.CreateView):
    if request.user.is_authenticated:
        _user = request.user.username
        data_base = getTable(_user)
    template_name = 'home.html'
