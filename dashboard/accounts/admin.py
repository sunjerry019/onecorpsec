from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import DatabaseUserCreationForm, DatabaseUserChangeForm
from .models import DatabaseUser

class DatabaseUserAdmin(UserAdmin):
    add_form = DatabaseUserCreationForm
    form = DatabaseUserChangeForm
    model = DatabaseUser
    list_display = ['email', 'username', 'name', 'sign_off_name']

admin.site.register(DatabaseUser, DatabaseUserAdmin)
