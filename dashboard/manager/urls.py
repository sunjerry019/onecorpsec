from django.urls import re_path, path, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', views.render_Home, name='home'),
    path('update/', views.updateDatabase, name="update"),
    re_path(r'^(\d+)/', views.render_Home),
]
