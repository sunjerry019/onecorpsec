#!/usr/bin/env python3

"""
This script is meant to check against the database for all the tables to see whether emails are to be sent.
If so, emails are sent using sendEmailWithTemplate.py
"""

# NOTE: No input sanitization is done here as input are supposed to be safe
# REVIEW: Email sending conditions, stop conditions not tested

import mysql.connector
from db import Database
import datetime
from datetime import datetime as dt
# from dateutil.relativedelta import relativedelta
# https://stackoverflow.com/a/15155212

class NXError(Exception):
    pass

class Checker():
    def __init__(self, user = False):
        self.database = Database()
        self.database.connect()
        self.users = self.getUsers()

        if user:
            if user not in self.users:
                raise NXError("User does not have a valid table")
            else:
                self.users = [user]

        self.today = dt.now()

        # columns should be the same for every one
        self.columnMap = self.database.query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'table_{}';".format(self.users[0]), None, True)
        self.columnMap = [x[0] for x in self.columnMap]

        # Audit                             => QUESTION: Unconfirmed whether we need this
        self.types = ["AGM", "GST", "IRAS", "audit"]

    def stopEmail(self, _usr, _CRN, _typ):
        # REVIEW: Test this part

        # First update the database flag
        self.updateDatabase(_usr, _typ + "_done", _CRN, 1)

        # Check if all 3 type are done
        # If all 3 types are done, update the financial year and reset all the flags
        # x = sum([self.getField(_usr, _CRN, t + "_done") for t in self.types])
        _x = 0
        for _t in self.types:
            _x += self.getField(_usr, _CRN, _t + "_done")

        if _x == 3:
            # Increase financial year by 1
            self.updateDatabaseDelta(_usr, _CRN, "fin_endYear", 1)
            for _t in self.types:
                self.updateDatabase(_usr, _CRN, _t + "_done", 0)
                # TODO: Reset email_next

    def runCheckAll(self):
        if self.users:
            # Run the checks here
            for user in self.users:
                self.runCheck(user)
        else:
            print("No users with appropriate data")

    def runCheck(self, user):
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

            for _typ in self.types:
                _done       = _a["{}_done".format(_typ)]
                _req        = _a["{}_req".format(_typ)] if _typ in ["GST", "audit"] else True

                if _req and not _done:
                    _yearEnd  = dt(_a["fin_endYear"], _a["fin_endMonth"], 1)
                    _nextEmail = dt(_a["fin_endYear"], _a[_typ + "_next"], 1) if (_a[_typ +"_next"] >= _a["fin_endMonth"]) else dt(_a["fin_endYear"] + 1, _a[_typ + "_next"], 1)

                    # IRAS only check until Nov 20; Set limit for checking (1 Year)
                    _finalEmail = dt(_a["fin_endYear"], 11, 30) if _typ is "IRAS" else dt(_a["fin_endYear"] + 1, _a["fin_endMonth"], 1)

                    if _yearEnd <= self.today <= _finalEmail and self.today >= _nextEmail and self.sendEmail(user, _a["coyRegNo"] , _typ):
                        # If any of the previous conditions don't match, the conditional will shortcircuit and not send the email
                        # Only update the database if the email sending is sucessful
                        self.updateDatabaseDelta(user, _a["coyRegNo"], "{}_next".format(_typ), _interval[_typ])

                    if self.today >= _finalEmail:
                        # we mark the item as if its done since its the final email we are going send anyway
                        self.stopEmail(user, _a["coyRegNo"], _typ)

    def getField(self, _usr, _CRN, _field):
        # returns the first result for the user, CRN and field
        # usually no more than 1 result will be returned
        return self.database.query("SELECT `{}` FROM `table_{}` WHERE `coyRegNo`='{}';".format(_field, _usr, _CRN), None, True)[0][0]

    def updateDatabase(self, _usr, _CRN, _field, _val):
        return self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}';".format(_usr, _field, _val, _CRN))

    def updateDatabaseDelta(self, _usr, _CRN, _field, _increment):
        _prevVal = self.database.query("SELECT `{}` FROM `table_{}` WHERE `coyRegNo`='{}';".format(_field, _usr, _CRN), None, True)[0][0]
        _newVal = _prevVal + _increment
        return self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}';".format(_usr, _field, _newVal, _CRN))

    def sendEmail(self, _usr, _coy, _typ):
        print("{} - {}: Sending Email for {}".format(_usr, _coy, _typ))

        # TODO: actually send the email
        return True

    def getUsers(self):
        # This function returns a list of users with a user database table
        # Users without a database table will not be returned

        users = []
        _users = self.database.query("SELECT username FROM `{}`".format(self.database.configurations["userTable"]), None, True)
        for user in _users:
            _r = self.database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'table_{}'".format(user[0]), None, True)
            if len(_r):
                users.append(user[0])
        return users

    def clean(self):
        # Cleanly close the Database
        self.database.exitDB()


def _main():
    x = Checker()
    x.runCheckAll()
    x.clean()

if __name__ == "__main__":
    _main()
