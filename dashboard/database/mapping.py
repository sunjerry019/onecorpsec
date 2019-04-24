#!/usr/bin/env python3

import csv
import argparse
from db import Database
import os

class NXFileError(Exception):
    pass

class Mapping():
    def __init__(self, csv = None, delete = False, configLocation = None):
        print(configLocation)
        self.database = Database(configLocation) if configLocation else Database()
        self.database.connect()
        self.csv = csv
        self.table = 'csv_mapping'
        self.delete = delete

    def createTableIfDoesntExist(self):
        # Check if the table already exists
        _r = self.database.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{}'".format(self.table), None, True)

        if len(_r) == 0:
            # Create the table
            _q = ("CREATE TABLE `{}` ("
                "sn SERIAL, "
                "tabletext VARCHAR (250) UNIQUE, "
                "plaintext VARCHAR (250), "
                "PRIMARY KEY (sn) "
                ");"
            ).format(self.table)

            self.database.query(_q)

    def importMap(self, _csv = None):
        # CSV is in the format of Plaintext, tabletext

        if not _csv: _csv = self.csv
        if not _csv: raise NXFileError("No file to import from")

        with open(_csv, 'r') as f:
            self.createTableIfDoesntExist()
            _reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in _reader:
                self.database.query("INSERT INTO `{}` (`tabletext`,`plaintext`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `tabletext`=%s, `plaintext`=%s;".format(self.table), (row[1], row[0], row[1], row[0]))

        if self.delete:
            try:
                os.remove(self.csv)
            except OSError:
                self.logfile.write("Unable to delete csv file\n")

    def getMap(self):
        ret = dict()
        _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
        for c in _columns:
            ret[c[2]] = c[1]

        return ret

    def getOrderedMap(self):
        ret = dict()
        order = list()
        _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
        for c in _columns:
            order.append(c[2])
            ret[c[2]] = c[1]

        return order, ret

    def getInverseOrderedMap(self):
        ret = dict()
        order = list()
        _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
        for c in _columns:
            order.append(c[1])
            ret[c[1]] = c[2]

        return order, ret

    def getInverseMap(self):
        ret = dict()
        _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
        for c in _columns:
            ret[c[1]] = c[2]

        return ret

    def generateTemplate(self, outputCSV = None):
        _csv = outputCSV
        if not _csv: _csv = self.csv
        # if not _csv: raise NXFileError("No file to export to")

        if _csv:
            with open(_csv, 'w') as f:
                # First write the serial number
                f.write('"S/N"')
                _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
                for c in _columns:
                    f.write(',"{}"'.format(c[2]))
        else:
            x = list()
            x.append('"S/N"')
            _columns = self.database.query("SELECT * FROM {}".format(self.table), None, True)
            for c in _columns:
                x.append(',"{}"'.format(c[2]))
            return "".join(x)

    def clean(self):
        self.database.exitDB()

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type = str, help = "csv file to parse or output to")
    parser.add_argument('-d', '--delete', action='store_true', help = "add flag to delete csv file after script")
    parser.add_argument('-i', '--importCSV', action='store_true', help = "Import the CSV Map")
    parser.add_argument('-e', '--exportCSV', action='store_true', help = "Export the CSV Map into a template")
    args = parser.parse_args()

    x = Mapping(args.filename, args.delete)
    if args.importCSV:
        x.importMap()
    if args.exportCSV:
        x.generateTemplate()
    x.clean()

if __name__ == '__main__':
    _main()
