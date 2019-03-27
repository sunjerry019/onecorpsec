from django.db import models

# Create your models here.

def getTable(_usrname):
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        managed = False
        db_table = 'table_' + _usrname

    # app_label must be set using the Meta inner class
    setattr(Meta, 'app_label', "manager")
    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': '', 'Meta': Meta}
    attrs.update({
        'sn'            : models.BigAutoField(primary_key=True),
        'coyname'       : models.CharField(db_column='coyName', max_length=250, blank=True, null=True),                 # Field name made lowercase.
        'coyregno'      : models.CharField(db_column='coyRegNo', unique=True, max_length=10, blank=True, null=True),    # Field name made lowercase.
        'toemail'       : models.CharField(db_column='toEmail', max_length=250, blank=True, null=True),                 # Field name made lowercase.
        'ccemail'       : models.CharField(db_column='ccEmail', max_length=250, blank=True, null=True),                 # Field name made lowercase.
        'bccemail'      : models.CharField(db_column='bccEmail', max_length=250, blank=True, null=True),                # Field name made lowercase.
        'addresseename' : models.CharField(db_column='addresseeName', max_length=250, blank=True, null=True),           # Field name made lowercase.
        'fin_endmonth'  : models.PositiveIntegerField(db_column='fin_endMonth', blank=True, null=True),                 # Field name made lowercase.
        'fin_endyear'   : models.IntegerField(db_column='fin_endYear', blank=True, null=True),                          # Field name made lowercase.
        'agm_next'      : models.IntegerField(db_column='AGM_next', blank=True, null=True),                             # Field name made lowercase.
        'agm_done'      : models.IntegerField(db_column='AGM_done', blank=True, null=True),                             # Field name made lowercase.
        'gst_req'       : models.IntegerField(db_column='GST_req', blank=True, null=True),                              # Field name made lowercase.
        'gst_endmonth'  : models.IntegerField(db_column='GST_endMonth', blank=True, null=True),                         # Field name made lowercase.
        'gst_done'      : models.IntegerField(db_column='GST_done', blank=True, null=True),                             # Field name made lowercase.
        'gst_type'      : models.IntegerField(db_column='GST_type', blank=True, null=True),                             # Field name made lowercase.
        'gst_next'      : models.IntegerField(db_column='GST_next', blank=True, null=True),                             # Field name made lowercase.
        'audit_req'     : models.IntegerField(blank=True, null=True),
        'audit_done'    : models.IntegerField(blank=True, null=True),
        'audit_next'    : models.IntegerField(blank=True, null=True),
        'iras_done'     : models.IntegerField(db_column='IRAS_done', blank=True, null=True),                            # Field name made lowercase.
        'iras_next'     : models.IntegerField(db_column='IRAS_next', blank=True, null=True)                             # Field name made lowercase.
    })

    # Create the class, which automatically triggers ModelBase processing
    model = type('UserTable', (models.Model,), attrs)

    return model
