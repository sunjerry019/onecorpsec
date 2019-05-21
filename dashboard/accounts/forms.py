from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import DatabaseUser
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES

# Groups
# from django.contrib.auth import get_user_model
# from django.contrib.admin.widgets import FilteredSelectMultiple
# from django.contrib.auth.models import Group

class DatabaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = DatabaseUser
        fields = ('username', 'email', 'reply_to', 'name', 'sign_off_name' )

    # https://overiq.com/django-1-10/django-creating-users-using-usercreationform/

    # def clean_username(self):
    #     username = self.cleaned_data['username'].lower()
    #     r = DatabaseUser.objects.filter(username=username)
    #     if r.count():
    #         raise ValidationError("Username already exists")
    #     return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = DatabaseUser.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        # user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        # if commit:
        #     user.save()
        if commit:
            self.cleaned_data["password"] = self.cleaned_data.pop("password1", None)
            self.cleaned_data.pop("password2", None)
            user = DatabaseUser.objects.create_user(**self.cleaned_data)
            return user
        return True

class DatabaseUserChangeForm(UserChangeForm):
    # fieldsets = (
    #         ('Basic Information', {'fields': ('email',)}),
    #         ('Personal info', {'fields': ('name', 'first_name', 'last_name', 'sign_off_name', 'reply_to',)}),
    #         ('Custom Email Server', {'fields': ('email_tls', 'email_host', 'email_port', 'email_host_user', 'email_host_pass',), "description": "Leave these blank to use the default onecorpsec.com mail servers."}),
    #     )

    class Meta:
        model = DatabaseUser
        fields = ('email', 'reply_to', 'name', 'first_name', 'last_name' , 'sign_off_name', 'email_tls', 'email_host', 'email_port', 'email_host_user', 'email_host_pass')

        widgets = {
            'email_host_pass': forms.PasswordInput(),
        }

    def clean(self):
        # https://stackoverflow.com/a/22816390/3211506
        super().clean()

        has_custom_host = self.cleaned_data.get('email_host', False)
        if has_custom_host:
            # validate the custom fields
            _fds  = ['email_tls', 'email_port', 'email_host_user'] # 'email_host_pass'
            _fdPT = ['TLS', 'Port', 'Host server username'] # 'Host server password'

            for i, fdname in enumerate(_fds):
                _fd  = self.cleaned_data.get(fdname, None)
                if _fd in EMPTY_VALUES:
                    self._errors[fdname] = self.error_class(['{} is required.'.format(_fdPT[i])])

        return self.cleaned_data


# # GROUPS = https://stackoverflow.com/a/39648244/3211506
# User = get_user_model()
#
# # Create ModelForm based on the Group model.
# class GroupAdminForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         exclude = []
#
#     # Add the users field.
#     users = forms.ModelMultipleChoiceField(
#          queryset=User.objects.all(),
#          required=False,
#          # Use the pretty 'filter_horizontal widget'.
#          widget=FilteredSelectMultiple('users', False)
#     )
#
#     def __init__(self, *args, **kwargs):
#         # Do the normal form initialisation.
#         super(GroupAdminForm, self).__init__(*args, **kwargs)
#         # If it is an existing group (saved objects have a pk).
#         if self.instance.pk:
#             # Populate the users field with the current Group users.
#             self.fields['users'].initial = self.instance.user_set.all()
#
#     def save_m2m(self):
#         # Add the users to the Group.
#         self.instance.user_set.set(self.cleaned_data['users'])
#
#     def save(self, *args, **kwargs):
#         # Default save
#         instance = super(GroupAdminForm, self).save()
#         # Save many-to-many data
#         self.save_m2m()
#         return instance
