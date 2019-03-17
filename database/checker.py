#!/usr/bin/env python3

"""
This script is meant to check against the database for all the tables to see whether emails are to be sent.
If so, emails are sent using sendEmailWithTemplate.py
"""

import mysql.connector
from db import Database

class Checker():
    def __init__(self):
        self.database = Database()
        self.database.connect()
        self.users = self.getUsers()

        if self.users:
            # Run the checks here
            
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
    x.clean()

if __name__ == "__main__":
    _main()
