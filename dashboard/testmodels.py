# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsDatabaseuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    name = models.CharField(max_length=250)
    sign_off_name = models.CharField(max_length=250)
    reply_to = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'accounts_databaseuser'


class AccountsDatabaseuserGroups(models.Model):
    databaseuser = models.ForeignKey(AccountsDatabaseuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_databaseuser_groups'
        unique_together = (('databaseuser', 'group'),)


class AccountsDatabaseuserUserPermissions(models.Model):
    databaseuser = models.ForeignKey(AccountsDatabaseuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_databaseuser_user_permissions'
        unique_together = (('databaseuser', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CsvMapping(models.Model):
    sn = models.BigAutoField(primary_key=True)
    tabletext = models.CharField(unique=True, max_length=250, blank=True, null=True)
    plaintext = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'csv_mapping'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsDatabaseuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TableAdmin(models.Model):
    sn = models.BigAutoField(primary_key=True)
    coyname = models.CharField(db_column='coyName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    coyregno = models.CharField(db_column='coyRegNo', unique=True, max_length=10, blank=True, null=True)  # Field name made lowercase.
    toemail = models.CharField(db_column='toEmail', max_length=250, blank=True, null=True)  # Field name made lowercase.
    ccemail = models.CharField(db_column='ccEmail', max_length=250, blank=True, null=True)  # Field name made lowercase.
    bccemail = models.CharField(db_column='bccEmail', max_length=250, blank=True, null=True)  # Field name made lowercase.
    addresseename = models.CharField(db_column='addresseeName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    fin_endmonth = models.PositiveIntegerField(db_column='fin_endMonth', blank=True, null=True)  # Field name made lowercase.
    fin_endyear = models.IntegerField(db_column='fin_endYear', blank=True, null=True)  # Field name made lowercase.
    agm_next = models.IntegerField(db_column='AGM_next', blank=True, null=True)  # Field name made lowercase.
    agm_done = models.IntegerField(db_column='AGM_done', blank=True, null=True)  # Field name made lowercase.
    gst_req = models.IntegerField(db_column='GST_req', blank=True, null=True)  # Field name made lowercase.
    gst_endmonth = models.IntegerField(db_column='GST_endMonth', blank=True, null=True)  # Field name made lowercase.
    gst_done = models.IntegerField(db_column='GST_done', blank=True, null=True)  # Field name made lowercase.
    gst_type = models.IntegerField(db_column='GST_type', blank=True, null=True)  # Field name made lowercase.
    gst_next = models.IntegerField(db_column='GST_next', blank=True, null=True)  # Field name made lowercase.
    audit_req = models.IntegerField(blank=True, null=True)
    audit_done = models.IntegerField(blank=True, null=True)
    audit_next = models.IntegerField(blank=True, null=True)
    iras_done = models.IntegerField(db_column='IRAS_done', blank=True, null=True)  # Field name made lowercase.
    iras_next = models.IntegerField(db_column='IRAS_next', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'table_admin'


class Users(models.Model):
    sn = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=128, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    salt = models.CharField(max_length=64, blank=True, null=True)
    tablename = models.CharField(db_column='tableName', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
