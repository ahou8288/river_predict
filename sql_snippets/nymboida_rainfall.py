# Database
import sqlite3

conn = sqlite3.connect('../old_dataset/mydb.db')
c = conn.cursor()

c.execute('SELECT year, month, day, rainfall FROM rainfall WHERE station_id = '+str(58045))

data= c.fetchall()

print(data)
print(len(data))
