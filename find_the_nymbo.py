# Database
import sqlite3

conn = sqlite3.connect('mydb.db')
c = conn.cursor()

nymbo_gauge=204001
nymbo_station=59124

c.execute('SELECT * FROM gauges WHERE id = '+str(nymbo_gauge))

nymbo_id,name,lat,log,elev=c.fetchone()
print(lat)
print(log)

c.execute('''
	SELECT *
	FROM stations
	ORDER BY (lat-({0}))*(lat-({0})) + (long-({1}))*(long-({1}))
	LIMIT 10'''.format(lat,log))
for i in c.fetchall():
	print(i)