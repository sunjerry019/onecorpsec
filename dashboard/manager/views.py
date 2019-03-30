from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.http import HttpResponse
from .models import getTable


def render_Home(request):
    t = get_template('home.html')
    _model = getTable(request.user.username)
    rows = _model.objects.all()
    html = t.render({ 'hostname': "OneCorpSec" , 'user': request.user, 'rows': rows })
    return HttpResponse(html)
