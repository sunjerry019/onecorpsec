#!/usr/bin/env python3

"""
This script is meant to check against the database for all the tables to see whether emails are to be sent.
If so, emails are sent using mailer.py
"""

# NOTE: No input sanitization is done here as input are supposed to be safe
# REVIEW: Email sending conditions, stop conditions not tested

import mysql.connector
from db import Database
from mapping import Mapping
import datetime
from datetime import datetime as dt
# from dateutil.relativedelta import relativedelta
# https://stackoverflow.com/a/15155212
import sys
sys.path.insert(0, '../')
import mailer

from database.helpers import getEmailConfiguration

class NXError(Exception):
    pass

class Checker():
    def __init__(self, user = False, _map = False, _confLoc = None):
        # user = username
        # _map = list of column headers
        self.database = Database(_confLoc) if _confLoc is not None else Database()
        self.database.connect()
        self.users = self.getUsers()

        self.mailerCompany = None
        self.emailConnectionUser = None
        self.emailConnection = None

        if user:
            if user not in self.users:
                raise NXError("User does not have a valid table")
            else:
                self.users = {user: self.users[user]}

        if not _map:
            # columns should be the same for every one
            self.columnMap = self.database.query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'table_{}';".format(next(iter(self.users))), None, True)
            self.columnMap = [x[0] for x in self.columnMap]
        else:
            # Reduce database call if unnecessary
            self.columnMap = _map

        self.today = dt.now()

        # Audit                             => QUESTION: Unconfirmed whether we need this
        self.types    = ["AGM", "GST", "IRAS", "audit"]
        self.numtypes = 4
        self.optional = {"GST": 1, "audit": 1}

    def runCheckAll(self):
        if self.users:
            # Run the checks here
            for user in self.users:
                self.runCheck(user)
        else:
            print("No users with appropriate data")

    def runCheck(self, user):
        # We set this every time runCheck is run
        self.emailConnectionUser = user
        self.emailConnection = getEmailConfiguration(user)

        _companies = self.database.query("SELECT * FROM `table_{}`".format(user), None, True)
        for company in _companies:
            _a = dict(zip(self.columnMap, company))

            # Here we assume all values held in the table are valid and accurate
            # No error correction/catching is done here

            # AGM/ACRA, GST, Income Tax (IRAS)  => Only check until Nov 20
            _intervals = {
                "AGM"   : 1,
                "GST"   : _a["GST_type"],
                "IRAS"  : 2,
                "audit" : 1
            }

            # Check if all 3 type are done (where required)
            # If all 3 types are done, update the financial year and reset all the flags

            _okays = 0

            for _typ in self.types:
                _req        = _a["{}_req".format(_typ)] if _typ in self.optional else True
                _done       = _a["{}_done".format(_typ)]
                _markDone   = []
                if _done < 0: _done = 0

                if _req and not _done:
                    _yearEnd  = dt(_a["fin_endYear"], _a["fin_endMonth"], 1)
                    _nextEmail = dt(_a["fin_endYear"], _a[_typ + "_next"], 1) if (_a[_typ +"_next"] >= _a["fin_endMonth"]) else dt(_a["fin_endYear"] + 1, _a[_typ + "_next"], 1)

                    # IRAS only check until Nov 20; Set limit for checking (1 Year)
                    _finalEmail = dt(_a["fin_endYear"], 11, 30) if _typ is "IRAS" else dt(_a["fin_endYear"] + 1, _a["fin_endMonth"], 1)

                    if _yearEnd <= self.today <= _finalEmail and self.today >= _nextEmail and self.sendEmail(user, _a["coyRegNo"] , _typ, _a):
                        # If any of the previous conditions don't match, the conditional will shortcircuit and not send the email
                        # Only update the database if the email sending is sucessful
                        self.updateDatabaseDelta(user, _a["coyRegNo"], "{}_next".format(_typ), _intervals[_typ])

                    if self.today >= _finalEmail:
                        # we mark the item as if its done since its the final email we are going send anyway
                        _done = 1
                        _markDone.append(_typ)

                # Check for OKAYNESS
                # KV-Map:
                #    D'  D
                # R' 1   1
                # R  0   1

                _ok   = _done | (_req ^ 1)
                _okays += _ok

            if _okays == self.numtypes:
                # REVIEW: Test this part
                # Check if all 3 type are done (where required)
                # If all 3 types are done, update the financial year and reset all the flags
                # x = sum([self.getField(_usr, _CRN, t + "_done") for t in self.types])

                # Increase financial year by 1
                self.updateDatabaseDelta(user, _a["coyRegNo"], "fin_endYear", 1)
                _fields = []
                _vals   = []

                for _t in self.types:
                    _fields += [ "{}_done".format(_t), "{}_next".format(_t) ]
                    _vals   += [0, _a["fin_endMonth"]]
                    # NOTE: Marking GST as done stops emails until the next financial year!
                print(_fields, _vals)
                self.updateDatabaseFields(user, _a["coyRegNo"], _fields, _vals)
            else:
                # Update the _done fields in the database if they have changed
                if len(_markDone) > 0:
                    self.updateDatabaseFields(user, _a["coyRegNo"], _markDone, [1] * len(_markDone))

    def getField(self, _usr, _CRN, _field):
        # returns the first result for the user, CRN and field
        # usually no more than 1 result will be returned
        return self.database.query("SELECT `{}` FROM `table_{}` WHERE `coyRegNo`='{}';".format(_field, _usr, _CRN), None, True)[0][0]

    def getRow(self, _usr, _CRN):
        return self.database.query("SELECT * FROM table_{} WHERE 'coyRegNo' = '{}';".format(_usr, _CRN), None, True)[0]

    def updateDatabaseField(self, _usr, _CRN, _field, _val):
        return self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}';".format(_usr, _field, _val, _CRN))

    def updateDatabaseFields(self, _usr, _CRN, _fields, _vals):
        # _fields and _vals are list()s
        _q = ["UPDATE `table_{}` SET".format(_usr)] + ["{} = %s,".format(x) for x in _fields[:-1]] + ["{} = %s".format(_fields[-1])] + ["WHERE (`coyRegNo` = %s)"]
        _q = " ".join(_q)
        _vals.append(_CRN)

        self.database.query(_q, tuple(_vals))

    def updateDatabaseDelta(self, _usr, _CRN, _field, _increment):
        _prevVal = self.database.query("SELECT `{}` FROM `table_{}` WHERE `coyRegNo`='{}';".format(_field, _usr, _CRN), None, True)[0][0]
        _newVal = _prevVal + _increment
        return self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}';".format(_usr, _field, _newVal, _CRN))

    def sendEmail(self, _usr, _coy, _typ, _row):
        # print("{} - {}: Sending Email for {}".format(_usr, _coy, _typ))

        if self.mailerCompany is None or self.mailerCompany is not _coy:
            # Reuse mailer if same company
            self.mailer = mailer.Mail(
                user            = _usr,
                reply_to        = self.users[_usr]["reply_to"],
                sign_off_name   = self.users[_usr]["sign_off_name"],
                row             = _row,
                connection      = self.emailConnection
                )

            self.mailerMappingDict = {
                "AGM"   : self.mailer.send_acra,
                "GST"   : self.mailer.send_gst,
                "IRAS"  : self.mailer.send_iras,
                "audit" : self.mailer.send_audit
            }
            self.mailerCompany = _coy

        return self.mailerMappingDict[_typ]()

    def getUsers(self):
        # This function returns a list of users with a user database table
        # Users without a database table will not be returned

        users = {}
        _users = self.database.query("SELECT username, email, reply_to, sign_off_name FROM `{}`".format(self.database.configurations["userTable"]), None, True)
        for user in _users:
            _r = self.database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'table_{}'".format(user[0]), None, True)
            if len(_r):
                users[user[0]] = {
                    "email"         : user[1],
                    "reply_to"      : user[2] if len(user[2]) else user[1],
                    "sign_off_name" : user[3]
                }
        return users

    def clean(self):
        # Cleanly close the Database
        self.database.exitDB()


def _main():
    x = Checker(_confLoc = "../../config.location")
    x.runCheckAll()
    x.clean()

if __name__ == "__main__":
    _main()
