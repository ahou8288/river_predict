
#-----------------------------------------------------------------------------
# Database
import sqlite3
import csv
import os
import re
from datetime import datetime

conn = sqlite3.connect('mydb.db')
c = conn.cursor()

def dropTables():
	c.execute('DROP TABLE gauges')
	c.execute('DROP TABLE stations')
	conn.commit()

def createGaugesTable():
	c.execute('Drop TABLE Gagues')

	c.execute('''CREATE TABLE Gauges
         (id integer PRIMARY KEY, name text, lat NUMBER, long number, elev number)''')
	# Save (commit) the changes
	conn.commit()

def createStationsTable():
	c.execute('DROP TABLE Stations')

	c.execute('''CREATE TABLE Stations
         (id integer PRIMARY KEY, name text, opened_year integer, closed date, lat NUMBER, long number, elev number, state text)''')
	# Save (commit) the changes
	conn.commit()

def createRainfallTable():
	c.execute('DROP TABLE Rainfall')

	c.execute('''CREATE TABLE Rainfall
		(station_id integer, year integer, month integer, day integer,	rainfall number,
		period number, quality char(1),
		PRIMARY KEY (station_id, year, month, day) )
		''')

def createLevelsTable():
	c.execute('DROP TABLE Levels')

	c.execute('''CREATE TABLE Levels
		(gauge_id integer, year integer, month integer, day integer, level number,
		quality integer,
		PRIMARY KEY (gauge_id, year, month, day) )
		''')

def insertGaugesData():
	# Insert the rows of data
	reader = csv.reader(open('cleaning data/gaugesMeta.csv', 'r'))
	for field1, field2, field3, field4, field5 in reader:
		c.execute('INSERT INTO gauges (id, name, lat, long, elev) VALUES (?,?,?,?,?)', (int(field1), field2, float(field3), float(field4), float(field5)))
	conn.commit()

def insertStationsData():
	# Insert a row of data
	reader = csv.reader(open('cleaning data/stationsMeta.csv', 'r'))

	
	for station_id, name, opened_year, closed, lat, longi, elev, state in reader:
		try:
			closed_date = datetime.strptime(closed, '%b %d %Y') #30 Nov 1988
		except:
			closed_date = None

		#remove unkown elevations
		if elev == ' Unknown':
			elev = -9999

		c.execute('INSERT INTO stations (id, name, opened_year, closed, lat, long, elev, state) VALUES (?,?,?,?,?,?,?,?)', 
			(int(station_id), name, int(opened_year), closed_date, float(lat), float(longi), float(elev), state))
	conn.commit()

def insertRainfallData():
	for filename in os.listdir('cleaning data/sampleData/rainfallData/'):
		print(filename)
		reader = csv.reader(open('cleaning data/sampleData/rainfallData/' + filename, 'r'))
		next(reader) #skip header row

		for productCode, stationId, year, month, day, rainfall, period, quality in reader:
			try:
				rainfall = float(rainfall)
			except:
				rainfall = None

			try:
				period = int(period)
			except:
				period = None

			c.execute('INSERT INTO Rainfall (station_id, year, month, day, rainfall, period, quality ) VALUES (?,?,?,?,?,?,?)', 
				(int(stationId), int(year), int(month), int(day), rainfall, period, quality))
	conn.commit()	

def insertLevelsData():
	# done = [line.rstrip('\n') for line in open('cleaning data/sampleData/level_files_done.txt')]


	for filename in os.listdir('cleaning data/sampleData/riverlevels/'):
		# if filename not in done:
		reader = csv.reader(open('cleaning data/sampleData/riverlevels/' + filename, 'r'))
		gauge_id = next(reader)[1] #get gauge_id from first row
		print (filename)


		#skip a useless line
		next(reader)


		#either rainfal, , levels
		#or levels, qual, levels, qual, levels, qual
		#check if it has rainfall
		fileType = next(reader)[1]

		#skip another useless line
		next(reader)

		#figure out what kinda file it is
		if fileType == 'Level (Metres)':
			for row in reader:
				if row:
					date = row[0]
					level = row[1]
					qual = row[2]
					
					try:
						level = float(level)
					except:
						level = None

					match = re.search(r'(\d+)/(\d+)/(\d+)', date) #10/02/1908  8:00:00 AM
					day = match.group(1)
					month = match.group(2)
					year = match.group(3)

					c.execute('INSERT INTO Levels (gauge_id, year, month, day, level, quality ) VALUES (?,?,?,?,?,?)', 
					(int(gauge_id), int(year), int(month), int(day), level, qual))

		
		elif fileType == 'Rainfall (mm)':
			for row in reader:
				if row:
					date = row[0]
					level = row[3]
					qual = row[4]
					try:
						level = float(level)
					except:
						level = None

					match = re.search(r'(\d+)/(\d+)/(\d+)', date) #10/02/1908  8:00:00 AM
					day = match.group(1)
					month = match.group(2)
					year = match.group(3)

					c.execute('INSERT INTO Levels (gauge_id, year, month, day, level, quality ) VALUES (?,?,?,?,?,?)', 
					(int(gauge_id), int(year), int(month), int(day), level, qual))

		conn.commit()


def exportAllLocations():
	outputFile = open("coordinates.csv", "a")
	data = c.execute("select Stations.lat, Stations.long, 1 from Stations").fetchall()

	csv_out=csv.writer(outputFile)
	for row in data:
		csv_out.writerow(row)

	data = c.execute("select Gauges.lat, Gauges.long, 0 from Gauges").fetchall()

	csv_out=csv.writer(outputFile)
	for row in data:
		csv_out.writerow(row)


#createStationsTable()
# dropTables()
# createGaugesTable()
# insertGaugesData()

# createStationsTable()
# insertStationsData()

#exportAllLocations()


#createRainfallTable()
#insertRainfallData()
# print(c.execute("select distinct(station_id) from Rainfall limit 20").fetchall())
# print(c.execute("select count(*)- count(rainfall), count(rainfall) from Rainfall limit 20").fetchall())

# createLevelsTable()
# insertLevelsData()

# Table sizes
print(c.execute("select avg(level) from Levels").fetchone()[0])
print(c.execute("select count(*) from gauges").fetchone()[0])
print(c.execute("select count(*) from stations").fetchone()[0])
print(c.execute("select avg(rainfall) from Rainfall").fetchone()[0])

#Testing portion of nulls
# print(c.execute('''select gauge_id, null_portion, obs FROM
# 	 (	
# 		SELECT gauge_id, round((cast(count(*) as float) - count(level))/count(*), 2) as null_portion, count(*) as obs
# 		FROM Levels
# 		GROUP BY gauge_id
# 		HAVING round((cast(count(*) as float) - count(level))/count(*), 2) > 0.1
# 	) 
# 	limit 200''').fetchall())

#testing aboslute number of nulls
# print(c.execute('''select count(*)- count(level), gauge_id from Levels
# 	GROUP BY gauge_id
# 	HAVING count(*) - count(level) > 1000''').fetchall())

# c.execute('''DELETE FROM Levels WHERE level is NULL''')
# conn.commit()

# c.execute('''DELETE FROM Rainfall WHERE Rainfall is NULL''')
# conn.commit()

# print(c.execute("select * from Rainfall WHERE Rainfall is NULL Limit 200").fetchall())


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()