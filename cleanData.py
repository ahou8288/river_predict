import sqlite3
import numpy
import matplotlib.pyplot as plt


conn = sqlite3.connect('mydb.db')
c = conn.cursor()



#get list of distances from station to nearest gauge
def dist_stat_gauge():
	query = '''
	SELECT S.id, S.lat, S.long, min((G.lat - S.lat)*(G.lat - S.lat) + (G.long - S.long)*(G.long-S.long)) as min_dist 
	FROM Stations as S JOIN Gauges as G
	GROUP BY S.id
	HAVING min((G.lat - S.lat)*(G.lat - S.lat) + (G.long - S.long)*(G.long-S.long)) > 1
	'''	

	a = c.execute(query).fetchall()
	[print(element) for element in a]


#remove island stations > 20 000km away from nearest gauge
def cull_stations():
	islands = '''
		DELETE FROM Rainfall
		WHERE station_id IN (
			SELECT id from Rainfall JOIN Stations ON station_Id = id
			WHERE long>159
		)
	'''

	island_stations = '''
		DELETE FROM Stations
		WHERE long>159
	'''

	c.execute(islands)
	c.execute(island_stations)
	conn.commit()

#get list of distances from gauge to nearest station
def dist_gauge_stat():
	query = '''
	SELECT G.id, G.lat, G.long, min((G.lat - S.lat)*(G.lat - S.lat) + (G.long - S.long)*(G.long-S.long)) as min_dist 
	FROM Stations as S JOIN Gauges as G
	GROUP BY G.id
	HAVING min((G.lat - S.lat)*(G.lat - S.lat) + (G.long - S.long)*(G.long-S.long)) > 0.03
	'''	

	a = c.execute(query).fetchall()
	[print(element) for element in a]

#histogram of guages - time spent at each level
#produce a image file for each then manually check they look normal
def hist_gauges():
	query = '''
		SELECT ROUND(level, 2)    AS bucket,
       	COUNT(*)                    AS COUNT
		FROM   Levels
		GROUP BY bucket
	'''
	levels = c.execute(query).fetchall()
	# bins = levels[:][0]
	# levels = levels[:][1]
	#this takes too long
	[print(element) for element in levels]


#histogram of rainfall - common amounts of rainfall

#explore the character of guages and nearby stations
#plot rainfall against level at specific known combos
#dtermine the correlation at different amounts of delay offset. 


# dist_stat_gauge()
# dist_gauge_stat()
# hist_gauges()

# cull_stations()


# print(c.execute('''select distinct(gauge_id) from Levels 
# 	WHERE quality not in(1,2,3, 4, 5, 6, 7, 8,9,10,11,26,30,31,32,33,36,38,39,40,41,45,46,51,52,57,58,60,61,65,66,67,68,70,71,100,130,145, 201, 255)
# 	''').fetchall())
# print(c.execute("SELECT count(*) from Rainfall WHERE quality = 'N'").fetchall())
# print(c.execute("SELECT count(*) FROM Rainfall Where period is NULL and rainfall>0").fetchall())
# print(c.execute("SELECT gauge_id, avg(level) from Levels WHERE level>250 GROUP BY gauge_id").fetchall())

#this is too slow, send it to R
# stations = c.execute("SELECT id FROM stations").fetchall()
# for station in stations:
# 	data = c.execute('''SELECT SUM((rainfall-(SELECT AVG(rainfall) FROM Rainfall))*
#        (rainfall-(SELECT AVG(rainfall) FROM rainfall)) ) / (COUNT(rainfall)-1) AS Variance
# 		FROM Rainfall Where Station_id = ?''', station)
# 	print(data.fetchall())

def exportToCsv():
	rainfallQuery = '''SELECT station_id, year, month, day, rainfall, lat, long 
		FROM Rainfall JOIN Stations ON station_id = id
		'''
	rainfallData = c.execute(rainfallQuery)

	rainfallData.fetchall()

# exportToCsv()
c.execute("SELECT * FROM Rainfall limit 10000").fetchall()
conn.close()