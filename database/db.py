#!/usr/bin/env python3

"""
Class file for manipulating the MySQL database
Not meant to be run by itself
Update credentials here
"""

# https://pypi.org/project/mysql-connector-python/

import os
import json
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        # Source for the configuration file
        _confLoc = "../config.location"
        with open(_confLoc, 'r') as f:
            _confFile = os.path.join(os.path.dirname(os.path.abspath(_confLoc)), f.readlines()[0].strip())

        with open(_confFile, 'r') as f:
            _conf = json.load(f)
            self.credentials = {
                "host"       : _conf["host"],
                "user"       : _conf["user"],
                "password"   : _conf["password"],
                "database"   : _conf["database"]
            }

    def escape(self, _str):
        # return self.dbConn._cmysql.escape_string(_str)
        return str(self.dbConn._cmysql.escape_string(_str), 'utf-8')

    def connect(self):
        try:
            self.dbConn = mysql.connector.connect(**self.credentials)
            self.dbCursor = self.dbConn.cursor()
        except Error as e :
            print("Error while connecting to MySQL: \n{}".format(e))

    def query(self, _query, data = None, result = False):
        if type(data) is not tuple:
            data = (data,)

        self.dbCursor.execute(_query, data) if data else self.dbCursor.execute(_query)

        if result:
            return self.dbCursor.fetchall()
        else:
            return True

    def exitDB(self):
        if self.dbConn.is_connected():
            self.dbConn.commit()
            self.dbConn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.exitDB()



if __name__ is "__main__":
    print("This script does nothing when run by itself")