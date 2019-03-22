#!/usr/bin/env python3

"""
This script is meant to check against the database for all the tables to see whether emails are to be sent.
If so, emails are sent using sendEmailWithTemplate.py
"""

import mysql.connector
from db import Database
import datetime

class Checker():
    def __init__(self, user = False):
        self.database = Database()
        self.database.connect()
        self.users = self.getUsers()

        if user:
            if user not in users:
                raise NXError("User does not have a valid table")
            else:
                self.user = user

        self.today = datetime.datetime.now()

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
                    _emailDue = datetime.datetime(_a["yearEndYear"], _a["yearEndMonth"], 1)

        else:
            print("No users with appropriate data")

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
