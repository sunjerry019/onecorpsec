from django.shortcuts import render

# Create your views here.
from django.conf import settings

from django.template.loader import get_template
from django.core.paginator import Paginator
import django.http as http                            # Provides HttpResponse, HttpResponseForbidden, etc.
from .models import getTable
from django.views.decorators.csrf import ensure_csrf_cookie
import json

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
    return http.HttpResponse(html)

def updateDatabase(request):
    if request.user.is_authenticated:
        # Trigger the checker here after updating
        _enc = request.encoding if request.encoding else settings.DEFAULT_CHARSET
        _form = json.loads(json.loads(request.body.decode(_enc)))

        # We need to invert everything as checked = emails turned on = not done!!!
        for field in _form:
            if field.endswith("_done"): _form[field] ^= 1

        # https://stackoverflow.com/a/14771593/3211506
        _model = getTable(request.user.username)

        _row = _model.objects.get(coyregno = _form['CRN'])
        _updateFields = []
        _fields = [f.name for f in _model._meta.get_fields()]

        for field in _fields:
            # https://stackoverflow.com/a/11464112/3211506
            if field in _form and getattr(_row, field) != _form[field]:
                setattr(_row, field, _form[field])
                _updateFields.append(field)

        try:
            _row.save(force_update=True, update_fields=_updateFields)
            return http.HttpResponse(status=200)
        except:
            return http.HttpResponse(status=500)
    else:
        return http.HttpResponseForbidden()
