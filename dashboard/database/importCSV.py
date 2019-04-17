#!/usr/bin/env python3

"""
Script for importing CSV into the MySQL Database
"""

import csv
import os, sys
import argparse
import mysql.connector
from mysql.connector import Error
from db import Database
from mapping import Mapping
import re
from functools import reduce

class ImporterError(Exception):
    """Generic error for errors in this importer"""
    pass


class DatabaseImporter:
    def __init__(self, filename, username, delete = False, logfile = sys.stdout):
        # Initialize all variables and parameters
        # Must ensure username parameter is safe

        self.delete = delete
        self.csvname = filename
        self.csvfile = open(self.csvname, 'r')
        self.database = Database()
        self.username = username

        self.sqlMapping = Mapping().getMap()

        if isinstance(logfile, str) and len(logfile) > 0:
            self.logfile = open(logfile, 'a')

        # connect to the database
        self.database.connect()
        self.table = self.getTableName()

    def getTableName(self):
        # _results = self.database.query("SELECT `tableName` FROM `users` WHERE (`user` = %s);", (self.database.escape(self.username)), True)
        # return _results[0][0]
        return "table_{}".format(self.username)

    def createTableIfDoesntExist(self):
        # Check if the table already exists
        _r = self.database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{}'".format(self.table), None, True)

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
            ).format(self.table)

            self.database.query(_q)

    def mapValues(self, ele):
        _ele = ele.upper()
        # Change Booleans
        # Changes all FALSE and TRUE values to 0 and 1
        if _ele == "FALSE":
            return 0
        elif _ele == "TRUE":
            return 1

        # Change Months
        monthMap = { "JAN" : 1, "FEB" : 2, "MAR" : 3, "APR" : 4, "MAY" : 5, "JUN" : 6, "JUL" : 7, "AUG" : 8, "SEP" : 9, "OCT" : 10, "NOV" : 11, "DEC" : 12 }
        if _ele in monthMap:
            return(monthMap[ele])

        # Change GST Type
        GSTTypeMap = {"1/12": 1, "3/12": 3, "6/12" : 6}
        if _ele in GSTTypeMap:
            return(GSTTypeMap[_ele])

        # Final test to change any string of integers into integers
        try:
            if isinstance(ele, str):
                ele = int(ele)
        except ValueError as e:
            pass

        return ele

    def removeTrailingCommas(self, _str):
        lastCharTest = re.compile(r"[a-z0-9]", re.IGNORECASE)

        while _str and not lastCharTest.match(_str[-1]):
            _str = _str[:-1]

        return _str

    def checkRowValid(self, row, _map):
        # ALSO takes the opportunity to clean up the row

        # https://stackoverflow.com/a/201378/3211506
        emailTest = re.compile(r"^(?:(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]),\s*)*(?:(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))$", re.MULTILINE | re.IGNORECASE)

        toemail  = self.removeTrailingCommas(row[_map.index("toEmail")])
        ccemail  = self.removeTrailingCommas(row[_map.index("ccEmail")])
        bccemail = self.removeTrailingCommas(row[_map.index("bccEmail")])

        row[_map.index("toEmail")]  = toemail
        row[_map.index("ccEmail")]  = ccemail
        row[_map.index("bccEmail")] = bccemail

        # Check if all ? fields have been filled up
        _reqs = isinstance(row[_map.index("audit_req")], int) & isinstance(row[_map.index("GST_req")], int)
        if not _reqs:
            return row, False

        # Check months and done fields
        monthCols = [
            row[_map.index("fin_endMonth")],
            row[_map.index("AGM_next")],
            row[_map.index("IRAS_next")]
        ]
        doneCols = [
            row[_map.index("AGM_done")],
            row[_map.index("IRAS_done")]
        ]

        if row[_map.index("audit_req")]:
            monthCols.append(row[_map.index("audit_next")])
            doneCols.append(row[_map.index("audit_done")])
        else:
            row[_map.index("audit_done")] = -1
            row[_map.index("audit_next")] = -1

        if row[_map.index("GST_req")]:
            monthCols.append(row[_map.index("GST_endMonth")])
            monthCols.append(row[_map.index("GST_next")])
            # Should be a valid type 1, 3 or 6
            gstType = (row[_map.index("GST_type")] in {1: 0, 3: 0, 6: 0})
            doneCols.append(row[_map.index("GST_done")])
        else:
            gstType = True
            row[_map.index("GST_done")]     = -1
            row[_map.index("GST_endMonth")] = -1
            row[_map.index("GST_next")]     = -1
            row[_map.index("GST_type")]     = -1

        # Should be a valid month 1 - 12
        # monthCols = [ x for x in monthCols if x != "" ] # Remove any empty strings
        try:
            monthCols = reduce( (lambda x, y: (1 <= x <= 12) & (1 <= y <= 12)) , monthCols)
        except Exception as e:
            return row, False

        try:
            doneCols = reduce( (lambda x, y: (x == 0 or x == 1) & (y == 0 or y == 1)) , doneCols)
        except Exception as e:
            return row, False


        # Should be a valid year after 1900
        yearCol = row[_map.index("fin_endYear")] > 1900

        print(len(toemail) >= 3,  \
            emailTest.match(toemail), \
            (len(ccemail) == 0  or emailTest.match(ccemail)) ,  \
            (len(bccemail) == 0 or emailTest.match(bccemail)) , \
            doneCols, \
            monthCols , \
            gstType , \
            yearCol)

        return (row, len(toemail) >= 3 and \
            emailTest.match(toemail) and \
            (len(ccemail) == 0  or emailTest.match(ccemail)) and \
            (len(bccemail) == 0 or emailTest.match(bccemail)) and \
            monthCols and \
            gstType and \
            yearCol)

    def parse(self):
        # Prepare the database
        self.createTableIfDoesntExist()

        # parse the uploaded csv file and insert into mysql database
        # TODO Sanistize the input
        _reader = csv.reader(self.csvfile, delimiter=',', quotechar='"')
        _map = list()
        _rowcount = 0
        _colCount = 0

        _returnStatus = 0
        _returnOutput = "OK"

        for row in  _reader:
            row = row[1:]           # we ignore the serial number
            try:
                row = [self.mapValues(self.database.escape(x.strip())) for x in row]
            except:
                _srow = str(row)
                _el = " ..." if len(_srow) > 8 else ""
                if self.logfile: self.logfile.write("Error mapping values: {}".format(row))
                raise ImporterError("Error mapping values: {:8.8}{}".format(_srow, _el))

            if _rowcount == 0:      # Headers
                assert len(row) == len(self.sqlMapping.keys()), "Numbers of columns do not match database"
                try:
                    _map = [self.sqlMapping[x.strip()] for x in row]
                except Exception as e:
                    raise ImporterError("Error mapping headers")
                _colCount = len(_map)
            else:
                # Check if CRN exists
                assert _map.index("coyRegNo") > -1, "No CRN column found"
                assert len(row[_map.index("coyRegNo")]) > 0, "No CRN found on row {}".format(_rowcount + 1)

                # Check valid values
                row, rowValid = self.checkRowValid(row, _map)
                assert rowValid, "Invalid data/type in CSV for CRN = {}. Check again?".format(row[_map.index("coyRegNo")])

                # Check if exists
                # Prepared SQL Statements will force quotes, table name is assumed to be clean and inserted directly into the query.
                _r = self.database.query("SELECT * FROM `{}` WHERE (`coyRegNo` = %s);".format(self.table), (row[_map.index("coyRegNo")]), True)

                if len(_r) == 1:
                    # UPDATE table1 SET field1=new_value1 WHERE condition
                    _q = ["UPDATE `{}` SET".format(self.table)] + ["{} = %s,".format(x) for x in _map[:-1]] + ["{} = %s".format(_map[-1])] + ["WHERE (`sn` = %s)"]
                    _q = " ".join(_q)
                    row.append(_r[0][0])
                elif len(_r) == 0:
                    # INSERT INTO table1 (field1, field2, ...) VALUES (value1, value2, ...)
                    _q = "INSERT INTO `{}` ({}) VALUES ({})".format(self.table, ", ".join(_map), ", ".join(["%s"] * _colCount))
                else:
                    if self.logfile: self.logfile.write("Non-unique Identifier, CRN = {}!",format(row[_map.index("coyRegNo")]))
                    raise ImporterError("Non-unique Identifier, CRN = {}!",format(row[_map.index("coyRegNo")]))
                    return

                _q += ";"
                self.database.query(_q, tuple(row))

            _rowcount += 1

    def clean(self):
        # Cleanly close the Database
        self.database.exitDB()

        # Close and delete the uploaded file
        self.csvfile.close()
        if self.delete:
            try:
                os.remove(self.csvname)
            except OSError:
                if self.logfile: self.logfile.write("Unable to delete csv file\n")
                raise ImporterError("Unable to delete csv file")

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type = str, help = "csv file to parse")
    parser.add_argument('username', type = str, help = "username of the importer")
    parser.add_argument('-l', '--logfile', type = str, help = "logfile, defaults to stdout", default = None)
    parser.add_argument('-d', '--delete', action='store_true', help = "add flag to delete csv file after script")
    args = parser.parse_args()

    x = DatabaseImporter(args.filename, args.username, args.delete ,args.logfile)
    x.parse()
    # try: x.parse()
    # except: quit(1)
    # Check the return status using PHP and output accordingly #TODO
    x.clean()

if __name__ == "__main__":
    _main()
