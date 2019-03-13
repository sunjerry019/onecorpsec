#!/usr/bin/env python3

"""
File for importing CSV into the MySQL Database
"""

import csv
import os, sys
import argparse
import mysql.connector
from mysql.connector import Error
from db import Database

class DatabaseImporter:
    def __init__(self, filename, username, delete = False, logfile = None):
        # Initialize all variables and parameters
        # table name to be imported from the mysql db
        self.delete = delete
        self.csvname = filename
        self.csvfile = open(self.csvname, 'r')
        self.database = Database()
        self.username = username

        self.sqlMapping = {
            "Company Name"     : "coyName",
            "Company Reg. No." : "coyRegNo",
            "To Emails"        : "toEmail",
            "CC Emails"        : "ccEmail",
            "BCC Emails"       : "bccEmail",
            "Addressee"        : "addresseeName",
            "Year End"         : "yearEndMonth",
            "Year"             : "yearEndYear",
            "AGM Done"         : "agmDone",
            "GST Required"     : "GSTReq",
            "GST Done"         : "GSTDone",
            "Audit Required"   : "auditReq",
            "Audit Done"       : "auditDone",
            "Income Tax Done"  : "incomeTaxDone",
        }

        if logfile is not None:
            self.logfile = open(logfile, 'a')
        else:
            self.logfile = sys.stdout

        # connect to the database
        self.database.connect()
        self.table = self.getTableName()

    def getTableName(self):
        _results = self.database.query("SELECT `tableName` FROM `users` WHERE (`user` = '{}')".format(self.username), True)
        return _results[0][0]

    def parse(self):
        # parse the uploaded csv file and insert into mysql database
        # TODO Sanistize the input
        _reader = csv.reader(self.csvfile, delimiter=',', quotechar='"')
        _map = list()
        _rowcount = 0
        _colCount = 0

        for row in  _reader:
            row = row[1:]           # we ignore the serial number
            if _rowcount == 0:      # Headers
                _map = [self.sqlMapping[x.strip()] for x in row]
                _colCount = len(_map)
                print(_map)
            else:
                # Check if exists
                _r = self.database.query("SELECT * FROM `{}` WHERE (`coyRegNo` = '{}')".format(self.table, row[_map.index("coyRegNo")]), True)
                if len(_r) == 1:
                    # Update Instead
                    #TODO
                    for i in range(_colCount):
                        pass
                elif len(_r) == 0:
                    # Insert
                    _q = "INSERT INTO `{}` ({}) VALUES ({})".format(self.table, ", ".join(self._map), ", ".join(row))
                else:
                    self.logfile.write("Non-unique Identifier!")
                    quit(1)

                self.database.query()

            _rowcount += 1

    def clean(self):
        # Cleanly close the Database
        self.database.exitDB()

        # Close and delete the uploaded file
        self.csvfile.close()
        if self.delete:
            try:
                os.remove(self.filename)
            except OSError:
                self.logfile.write("Unable to delete csv file\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type = str, help = "csv file to parse")
    parser.add_argument('username', type = str, help = "username of the importer")
    parser.add_argument('-l', '--logfile', type = str, help = "logfile, defaults to stdout", default = None)
    parser.add_argument('-d', '--delete', action='store_true', help = "add flag to delete csv file after script")
    args = parser.parse_args()

    x = DatabaseImporter(args.filename, args.username, args.delete ,args.logfile)
    x.parse()
    x.clean()

if __name__ == "__main__":
    main()
