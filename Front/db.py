import sqlite3
from  .config import *

class Settings:

    @staticmethod
    def changeParams(file_path, car_value):
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute(f'INSERT INTO config (map, car_value) VALUES ("{file_path}", {car_value})')
        #cur.execute(f'UPDATE config SET map = "{file_path}", car_value = {car_value} ORDER BY id LIMIT 1')

        con.commit()
        con.close()

