from django.shortcuts import render

from django.conf import settings

from django.template.loader import get_template
from django.core.paginator import Paginator
import django.http as http                            # Provides HttpResponse, HttpResponseForbidden, etc.
from .models import getTable
from django.views.decorators.csrf import ensure_csrf_cookie
import json

# errors
from django.db.utils import ProgrammingError

# CSV Stuff
import sys, os
sys.path.insert(0, 'database/')
import checker, mapping, importCSV, exportCSV, helpers
from fileValidator import FileValidator
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str

import time

@ensure_csrf_cookie
def render_Home(request, page = 1):
    if request.user.is_authenticated:
        _model = getTable(request.user.username)
        try:
            all_rows = _model.objects.all().order_by('coyname')
            # attempt to access the object so it can error out if necessary
            _x = str(all_rows)
        except ProgrammingError as e:
            helpers.createTableIfDoesntExist(request.user.username)
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
        numitems = None

    # https://stackoverflow.com/a/13048311/3211506
    # Ensures CSRF
    return render(request, 'home.html', {
        'hostname'      : "OneCorpSec",
        'user'          : request.user,
        'rows'          : rows,
        'numitems'      : numitems,
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
                return http.HttpResponse(status=200)
            except Exception as e:
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

            # Preliminary check on document
            validate_file = FileValidator(max_size=52428800, content_types=('text/plain','text/csv')) # 52428800 B = 50 MiB
            try:
                validate_file(_file)
            except ValidationError as e:
                return http.HttpResponse(status=500, content=e)

            if not os.path.exists('./temp'):
                try:
                    os.makedirs('./temp')
                except OSError as e:
                    return http.HttpResponse(status=500, content=e)

            try:
                with open(_dest + ".csv", 'wb+') as destination:
                    for chunk in _file.chunks():
                        destination.write(chunk)
            # https://stackoverflow.com/a/4992124/3211506 (Does not catch KeyboardInterrupt, etc.)
            except Exception as e:
                # Remove file if exists
                if os.path.isfile(_dest + ".csv"):
                    os.remove(_dest + ".csv")
                return http.HttpResponse(status=500, content=e)

            # Import the CSV
            # delete = True, and no log files since we don't want to clog up the server
            di = importCSV.DatabaseImporter(_dest + ".csv", request.user.username, True, None)
            try:
                di.parse()
            except (importCSV.ImporterError, AssertionError) as e:
                di.clean()
                return http.HttpResponse(status=500, content=e)
            except Exception as e:
                di.clean()
                return http.HttpResponse(status=500, content="Unknown Parsing/Update Error")

            di.clean()
            return http.HttpResponse(content="OK")
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
                _model.objects.get(coyregno = _CRN).delete()
                return http.HttpResponse(status=200)
            except Exception as e:
                return http.HttpResponse(status=500)
        else:
            return http.HttpResponseNotAllowed("POST", content="GET Not Allowed")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

def download(request):
    if request.user.is_authenticated:
        return http.HttpResponseForbidden(content="Forbidden; Please access downloadable resources directly")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

def downloadDatabase(request):
    if request.user.is_authenticated:
        # sth here to get csv
        _ex = exportCSV.DatabaseExporter(request.user.username, None)
        try:
            _csvT = _ex.exportDB()
        except exportCSV.ExporterError as e:
            return http.HttpResponse(status=500, content=e)

        _ex.clean()

        # https://stackoverflow.com/a/1158750/3211506
        _res = http.HttpResponse(content=_csvT, content_type='text/csv')
        _res['Content-Disposition'] = 'attachment; filename={}'.format(smart_str("database.csv"))
        return  _res
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

def runPage(request):
    if request.user.is_authenticated:
        return http.HttpResponseForbidden(content="Forbidden; Please access endpoints directly. If you don't know the endpoint, you probably shouldn't run it. ")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

def manualChecker(request):
    if request.user.is_authenticated:
        try:
            c = checker.Checker()
            o = c.runCheck(request.user.username)
            c.clean()
            return http.HttpResponse(status=200, content="OK! Check done.<br>{}".format(o))
        except Exception as e:
            return http.HttpResponse(status=500, content=e)
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")

@ensure_csrf_cookie
def editMails(request):
    if request.user.is_authenticated:
        # https://stackoverflow.com/a/13048311/3211506
        # Ensures CSRF
        return render(request, 'emails.html', {
            'hostname' : "OneCorpSec",
            'user'     : request.user
        })
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")


def updateEmailTemplate(request, _type):
    if request.user.is_authenticated:
        if request.method == "POST":
            _file = request.FILES['file']

            # Process the files here
            

            return http.HttpResponse(status=200)
        else:
            return http.HttpResponseNotAllowed("POST", content="GET Not Allowed")
    else:
        return http.HttpResponseForbidden(content="Forbidden; Please Login")
