#!/usr/bin/env python3

from db import Database

def createTableIfDoesntExist(usrname):
    # This is a mirror of the function in importCSV.py
    # Please change this function as well if that function is changed in importCSV
    
    _database = Database()

    # connect to the database
    _database.connect()
    _table = "table_{}".format(usrname)

    # Check if the table already exists
    _r = _database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{}'".format(_table), None, True)

    if len(_r) == 0:
        # Create the table
        _q = ("CREATE TABLE `{}` ("
            "sn SERIAL, "
            "coyName VARCHAR(250) CHARACTER SET utf8, "          # Company Name
            "coyRegNo VARCHAR(10) CHARACTER SET utf8 UNIQUE , "  # Register No = Unique Identifier
            "toEmail VARCHAR(250) CHARACTER SET utf8, "          # To Emails (can have multiple, comma separated)
            "ccEmail VARCHAR(250) CHARACTER SET utf8, "          # CC Emails (can have multiple, comma separated)
            "bccEmail VARCHAR(250) CHARACTER SET utf8, "         # BCC Emails (can have multiple, comma separated)
            "addresseeName VARCHAR(250) CHARACTER SET utf8, "    # who the emails should be addressed to
            "fin_endMonth TINYINT(2) UNSIGNED, "                 # The month in an tiny int format
            "fin_endYear YEAR(4) UNSIGNED, "                     # The year in which the next ACRA is due
            "AGM_next TINYINT(2), "                              # The next month that the AGM email is to be sent.
            "AGM_done BOOLEAN, "                                 # Flag for whether need to continue sending AGM email
            "GST_req BOOLEAN, "                                  # Flag for whether company needs to submit GST
            "GST_endMonth TINYINT(2), "                          # End Month for GST
            "GST_done BOOLEAN, "                                 # Flag for whether need to continue sending GST Reminder Email
            "GST_type TINYINT(2), "                              # Type of GST (1/12 = Monthly, 3/12 = Quarterly, 6/12 = Semi-Annually)
            "GST_next TINYINT(2), "                              # The next month that the AGM email is to be sent.
            "audit_req BOOLEAN, "                                # Flag for whether company needs to submit GST
            "audit_done BOOLEAN, "                               # Flag for whether need to continue sending Audit Email
            "audit_next TINYINT(2), "                            # The next month that the audit email is to be sent.
            "IRAS_done BOOLEAN, "                                # Flag for whether need to continue sending Income Tax Email
            "IRAS_next TINYINT(2), "                             # The next month that the IRAS email is to be sent
            "PRIMARY KEY (sn) "
            ");"
        ).format(_table)

        _database.query(_q)