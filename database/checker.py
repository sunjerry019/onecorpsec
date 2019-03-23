#!/usr/bin/env python3

"""
This script is meant to check against the database for all the tables to see whether emails are to be sent.
If so, emails are sent using sendEmailWithTemplate.py
"""

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
                self.user = user

        self.today = dt.now()

        self.intervals = {
            "AGM": 1,
            "GST": 1,
            ""
        }

    def stopEmail(self, type, CRN):
        # Update the flag and check if all 3 type are GST_done
        # If all 3 types are done, update the financial year and reset all the flags

    def runCheckAll(self):
        if self.users:
            # Run the checks here
            # columns should be the same for every one
            self.columnMap = self.database.query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'table_{}';".format(self.users[0]), None, True)
            self.columnMap = [x[0] for x in self.columnMap]

            for user in self.users:
                _companies = self.database.query("SELECT * FROM `table_{}`".format(user), None, True)
                for company in _companies:
                    _a = dict(zip(self.columnMap, company))

                    # Here we assume all values held in the table are valid and accurate
                    # No error correction is done here

                    # AGM/ACRA, GST, Income Tax (IRAS)  => Only check until Nov 20
                    # Audit                             => QUESTION: Unconfirmed whether we need this

                    _types = ["agm", "GST", "IRAS"]
                    _intervals = {
                        "agm"  : 1,
                        "GST"  : _a["GST_type"],
                        "IRAS" : 2
                    }

                    for _typ in _types:
                        _done       = _a["{}_done".format(_typ)]
                        _req        = _a["GST_req"] if _typ is "GST" else True

                        if _req and not _done:
                            _yearEnd  = dt(_a["fin_endYear"], _a["fin_endMonth"], 1)
                            _nextEmail = dt(_a["fin_endYear"], _a["{}_next".format(_typ)], 1) if (_a["{}_next".format(_typ)] >= _a["fin_endMonth"]) else dt(_a["fin_endYear"] + 1, _a["{}_next".format(_typ)], 1)

                            # IRAS only check until Nov 20; Set limit for checking (1 Year)
                            _finalEmail = dt(_a["fin_endYear"], 11, 30) if _typ is "IRAS" else dt(_a["fin_endYear"] + 1, _a["fin_endMonth"], 1)

                            if _yearEnd <= self.today <= _finalEmail and self.today >= _nextEmail and self.sendEmail(user, _typ):
                                self.updateDatabaseDelta(user, _a["coyRegNo"], "{}_next".format(_typ), _interval[_typ])

        else:
            print("No users with appropriate data")

    def updateDatabase(self, _usr, _CRN, _field, _val):
        self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}'".format(_usr, _field, _val, _CRN))

    def updateDatabaseDelta(self, _usr, _CRN, _field, _incrementMonth):
        _prevVal = self.database.query("SELECT `{}` FROM `table_{}` WHERE `coyRegNo`='{}'".format(_field, _usr, _CRN), None, True)[0][0]
        _newVal = _prevVal + _incrementMonth
        self.database.query("UPDATE `table_{}`SET `{}`='{}' WHERE `coyRegNo`='{}'".format(_usr, _field, _newVal, _CRN))

    def sendEmail(self, _user, _typ):
        print(typ)
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
