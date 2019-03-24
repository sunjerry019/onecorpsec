#!/usr/bin/env python3

from db import Database

x = Database()
x.connect()
print(x.query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{}'".format("table_admin"), None, True))
x.exitDB()
