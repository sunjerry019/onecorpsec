from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False)), # https://stackoverflow.com/a/9093623/3211506
    path('signup/', views.SignUp.as_view(), name='signup'),
]
