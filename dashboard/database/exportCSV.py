#!/usr/bin/env python3

"""
Script for exporting CSV from the MySQL Database
"""

# import csv
import os, sys
import argparse
import mysql.connector
from mysql.connector import Error
from db import Database
from mapping import Mapping

class ExporterError(Exception):
    """Generic error for errors in this exporter"""
    pass

class DatabaseExporter:
    def __init__(self,  username, filename = None, configLocation = None):
        # Initialize all variables and parameters
        # Must ensure username parameter is safe

        self.csvname = filename
        self.database = Database(configLocation) if configLocation else Database()
        self.username = username

        self.sqlMappingOrder, self.sqlMapping = Mapping(configLocation = configLocation).getInverseOrderedMap()
        self.defineMaps()

        if isinstance(filename, str) and len(filename) > 0:
            self.csvfile = open(self.csvname, 'w')
        else:
            # if its None or sys.stdout
            self.csvfile = self.csvname

        # connect to the database
        self.database.connect()
        self.table = self.getTableName()

    def defineMaps(self):
        self.columns = len(self.sqlMappingOrder)
        # 1 = GST Type, 2 = Month Map, 3 = TRUE/FALSE
        self.mappableColumns = {
            "GST_type"      : 1,
            "fin_endMonth"  : 2,
            "AGM_next"      : 2,
            "AGM_done"      : 3,
            "GST_req"       : 3,
            "GST_endMonth"  : 2,
            "GST_done"      : 3,
            "GST_next"      : 2,
            "audit_req"     : 3,
            "audit_done"    : 3,
            "audit_next"    : 2,
            "IRAS_done"     : 3,
            "IRAS_next"     : 2

        }
        self.GSTTypeMap = { -1: "", 1: "1/12", 3: "3/12", 6: "6/12"}
        self.monthMap   = { -1: "", 1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC" }
        self.boolMap    = { -1: "", 0: "FALSE", 1: "TRUE" }

        def c_asis(ele):      return ele
        def c_month(ele):     return self.monthMap[ele]
        def c_gstType(ele):   return self.GSTTypeMap[ele]
        def c_boolean(ele):   return self.boolMap[ele]

        self.mapped = { 0: c_asis, 1: c_gstType, 2: c_month, 3: c_boolean }

    def getTableName(self):
        return "table_{}".format(self.username)

    def exportDB(self):
        # check if table exists
        _r = self.database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{}'".format(self.table), None, True)

        if len(_r) == 0: raise ExporterError("Table does not exist yet. Have you populated the database?")

        _ret = list()

        _companies = self.database.query("SELECT * FROM `{}`".format(self.table), None, True)

        # print headers
        # First write the serial number
        _headers = ['"S/N"']
        for c in self.sqlMappingOrder:
            _headers.append('"{}"'.format(self.sqlMapping[c]))

        _ret.append(",".join(_headers))

        _coyCount = 0
        for coy in _companies:
            _coy = coy[1:]
            _coyCount += 1

            _row = ['"{}"'.format(_coyCount)]

            for i in range(self.columns):
                # 0 = nomap, 1 = GST Type, 2 = Month Map, 3 = TRUE/FALSE
                _maptype = self.mappableColumns.get(self.sqlMappingOrder[i], 0)
                try:
                    _row.append('"{}"'.format(self.mapped[_maptype](_coy[i])))
                except (KeyError, IndexError):
                    raise ExporterError("Database data incorrect. Please contact administrator.")

            _ret.append(",".join(_row))

        _retJoined = "\n".join(_ret)

        if self.csvfile:
            self.csvfile.write(_retJoined)
            return

        return _retJoined

    def clean(self):
        # Cleanly close the Database
        self.database.exitDB()

        # Close the csvfile if open
        if self.csvfile:
            self.csvfile.close()

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type = str, help = "username of the exporter")
    parser.add_argument('-o', '--output', type = str, help = "csv file to export to, defaults to stdout", default = None)
    args = parser.parse_args()

    _o = args.output if (isinstance(args.output, str) and len(args.output) > 0) else sys.stdout
    x = DatabaseExporter(args.username, _o)
    x.exportDB()
    x.clean()

if __name__ == "__main__":
    _main()
