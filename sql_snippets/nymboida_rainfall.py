# Database
import sqlite3
import csv
import datetime

conn = sqlite3.connect('../old_dataset/mydb.db')
c = conn.cursor()

print('Executing SQL.')
c.execute(
    'SELECT year, month, day, rainfall FROM rainfall WHERE station_id = ' + str(58045))

data = c.fetchall()

for i in range(len(data)):
    date = datetime.datetime(
        year=data[i][0],
        month=data[i][1],
        day=data[i][2],
        hour=9)
    time_str = date.strftime('%Y-%m-%d %H:%M:%S')
    data[i] = [time_str, data[i][3]]

print('Writing to file.')
with open('../old_dataset/nymboida_rain.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Date", "Rainfall"])
    wr.writerows(data)

print('Finished.')
