# Database
import sqlite3
import csv

conn = sqlite3.connect('../old_dataset/mydb.db')
c = conn.cursor()

c.execute('SELECT year, month, day, rainfall FROM rainfall WHERE station_id = '+str(58045))

data = c.fetchall()
import csv

with open('../old_dataset/nymboida_rain.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
    wr.writerows(data)