import os
from .config import *
import sqlite3

def getParams():
    result = []

    con = sqlite3.connect(db)
    cur = con.cursor()
    query = cur.execute('SELECT * FROM config ORDER BY id DESC LIMIT 1')
    for row in query:
        result.append(row[1])
        result.append(row[2])
        result.insert(0, 'set')

    return result


