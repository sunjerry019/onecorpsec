from .forms import DatabaseUserCreationForm, DatabaseUserChangeForm
# from .forms import GroupAdminForm
from .models import DatabaseUser

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class DatabaseUserAdmin(UserAdmin):
    add_form = DatabaseUserCreationForm
    form = DatabaseUserChangeForm
    model = DatabaseUser
    list_display = ['email', 'username', 'name', 'sign_off_name']
    # https://stackoverflow.com/a/24438757/3211506
    fieldsets = (
            ('Basic Information', {'fields': ('username', 'password',), 'description': '<b style="color:red;">DO NOT EDIT THESE!</b>'}),
            ('Personal info', {'fields': ('name', 'first_name', 'last_name', 'sign_off_name', 'email', 'reply_to', 'date_joined', 'last_login',)}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
            ('Custom Email Server', {'fields': ('email_tls', 'email_host', 'email_port', 'email_host_user', 'email_host_pass',), 'description': 'Leave these blank to use the default onecorpsec.com mail servers. <b style="color: red;">Always remember to test your mail settings after setting it!</b>'}),
        )
    search_fields = ('id', 'username', 'email', 'name', 'first_name', 'last_name',)
    ordering = ('username',)

    # If you ever want to add groups to the list_display
    # https://stackoverflow.com/a/31195602/3211506

admin.site.register(DatabaseUser, DatabaseUserAdmin)

# # Unregister the original Group admin.
# admin.site.unregister(Group)
#
# # Create a new Group admin.
# class GroupAdmin(admin.ModelAdmin):
#     # Use our custom form.
#     form = GroupAdminForm
#     # Filter permissions horizontal as well.
#     filter_horizontal = ['permissions']
#
# # Register the new Group ModelAdmin.
# admin.site.register(Group, GroupAdmin)
