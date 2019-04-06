from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import getTable
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def render_Home(request, page = 1):
    t = get_template('home.html')
    if request.user.is_authenticated:
        _model = getTable(request.user.username)
        all_rows = _model.objects.all().order_by('coyname')

        numitems = request.session['enum'] if 'enum' in request.session else 25
        numitems = request.GET.get('enum') or numitems
        request.session['enum'] = numitems

        _p = Paginator(all_rows, numitems)
        rows = _p.get_page(page)
        override_base = None
    else:
        rows = None
        all_rows = []
        override_base = "base.html"

    html = t.render({
        'hostname'      : "OneCorpSec",
        'user'          : request.user,
        'rows'          : rows,
        'rowCount'      : len(all_rows),
        'override_base' : override_base
    })
    return HttpResponse(html)

def updateDatabase(request):
    # Trigger the checker here after updating
    print(request.POST)
    return HttpResponse()
