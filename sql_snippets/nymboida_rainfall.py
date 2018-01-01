# Database
import sqlite3
import csv

conn = sqlite3.connect('../old_dataset/mydb.db')
c = conn.cursor()

print('Executing SQL.')
c.execute(
    'SELECT year, month, day, rainfall FROM rainfall WHERE station_id = ' + str(58045))

data = c.fetchall()

for i in range(len(data)):
    data[i] = [
        '{}/{}/{}'.format(data[i][2], data[i][1], data[i][0]),
        data[i][3]
    ]

print('Writing to file.')
with open('../old_dataset/nymboida_rain.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(data)

print('Finished.')
