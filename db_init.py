# coding:utf-8

import sqlite3

con = sqlite3.connect('test.db')

try:
    con.executescript('db_init.sql')
except Exception as e:
    print e
finally:
    con.close()
