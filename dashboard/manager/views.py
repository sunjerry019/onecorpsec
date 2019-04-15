from django.shortcuts import render

from django.conf import settings

from django.template.loader import get_template
from django.core.paginator import Paginator
import django.http as http                            # Provides HttpResponse, HttpResponseForbidden, etc.
from .models import getTable
from django.views.decorators.csrf import ensure_csrf_cookie
import json

# CSV Stuff
import sys
sys.path.insert(0, 'database/')
import checker, mapping, importCSV
from django.utils.encoding import smart_str

import time

@ensure_csrf_cookie
def render_Home(request, page = 1):
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

    # https://stackoverflow.com/a/13048311/3211506
    # Ensures CSRF
    return render(request, 'home.html', {
        'hostname'      : "OneCorpSec",
        'user'          : request.user,
        'rows'          : rows,
        'rowCount'      : len(all_rows),
        'override_base' : override_base
    })

def updateDatabase(request):
    if request.user.is_authenticated:
        if request.method == "POST":
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

            # Update the Database
            try:
                _row.save(force_update=True, update_fields=_updateFields)

                # TODO: If successful, trigger the checker here for that username for that company

                return http.HttpResponse(status=200)
            except:
                return http.HttpResponse(status=500)
        else:
            return http.HttpResponseNotAllowed("POST", content="GET Not Allowed")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")


def updateDatabaseCSV(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            _file = request.FILES['file']
            _dest = './temp/{}_{}'.format(request.user, int(time.time()))

            with open(_dest + ".csv", 'wb+') as destination:
                for chunk in _file.chunks():
                    destination.write(chunk)

            # TODO: Check for CSV file here

            # Import the CSV
            di = importCSV.DatabaseImporter(_dest + ".csv", request.user, True, _dest + ".log")
            try:
                _status, _output = di.parse()
                if _status != 0:
                    return http.HttpResponse(status=500, content=_output)
            except:
                return http.HttpResponse(status=500, content="Unknown Parsing/Update Error")

            di.clean()

            return http.HttpResponse()
        else:
            # If not POST, we generate a template for the csv
            m = mapping.Mapping()
            _csvT = m.generateTemplate()

            # https://stackoverflow.com/a/1158750/3211506
            _res = http.HttpResponse(content=_csvT, content_type='text/csv')
            _res['Content-Disposition'] = 'attachment; filename={}'.format(smart_str("template.csv"))
            return  _res
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

def deleteCompany(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            _enc = request.encoding if request.encoding else settings.DEFAULT_CHARSET
            _form = json.loads(json.loads(request.body.decode(_enc)))
            _CRN = _form["CRN"]

            # https://stackoverflow.com/a/14771593/3211506
            _model = getTable(request.user.username)
            
            # Update the Database
            try:
                # Some code here to delete
                return http.HttpResponse(status=200)
            except:
                return http.HttpResponse(status=500)
        else:
            return http.HttpResponseNotAllowed("POST", content="GET Not Allowed")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")
