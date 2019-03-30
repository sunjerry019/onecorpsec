from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.http import HttpResponse
from .models import getTable


def render_Home(request):
    t = get_template('home.html')
    if request.user.is_authenticated:
        _model = getTable(request.user.username)
        rows = _model.objects.all()
    else:
        rows = []
    html = t.render({ 'hostname': "OneCorpSec" , 'user': request.user, 'rows': rows, 'rowCount': len(rows) })
    return HttpResponse(html)
