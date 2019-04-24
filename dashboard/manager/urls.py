from django.urls import re_path, path, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', views.render_Home, name='home'),
    path('emails/', views.editMails, name="editMails"),
    path('run/checker/', views.manualChecker, name="runChecker"),
    path('run/', views.runPage, name="run"),
    path('download/database/', views.downloadDatabase, name="download_db"),
    path('download/', views.download, name="download"),
    path('update/csv/', views.updateDatabaseCSV, name="update_csv"),
    re_path(r'^update/template/(html|txt)/', views.updateEmailTemplate, name="updateEmailTemplate"),
    path('update/', views.updateDatabase, name="update"),
    path('delete/', views.deleteCompany, name="delete"),
    re_path(r'^(\d+)/', views.render_Home),
]
