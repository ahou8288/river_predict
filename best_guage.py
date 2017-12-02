import sqlite3

conn = sqlite3.connect('mydb.db')


def sql(query, many=True):
    c = conn.cursor()
    c.execute(query)
    if many:
        query_result = c.fetchall()
    else:
        query_result = c.fetchone()
    c.close()
    return query_result


def distance(a, b, c, d):
    return ((a - c)**2 + (b - d)**2)**0.5


def log(msg):
    print(msg)

def show_plot(gauge_info,stations,threshold):
    # create a plot with size of threshold
    # create a labeled center point with the gauges info
    # create a circle showing the threshold
    # put each station on the plot


log('Loading gauge info')
gauges = sql('SELECT id, lat, long FROM gauges')

# data storage as global
gauge_distance = {}

# station opening year
log('Finding station opening year.')
station_opening = {}
for station in sql('SELECT station_id, min(year) FROM rainfall GROUP BY station_id'):
    station_opening[station[0]] = station[1]

station_info = sql('SELECT id, lat, long, opened_year FROM stations')

log('Constructing distance matrix.')
for gauge in gauges:
    g_id, g_lat, g_long = gauge
    gauge_distance[g_id] = []
    for station in station_info:
        s_id, s_lat, s_long, s_opened_year = station
        gauge_distance[g_id].append(
            (s_id, distance(g_lat, g_long, s_lat, s_long)))

log('Selecting relevant gauges.')
distance_threshold = 0.05
for gauge in gauges:
    g_id = gauge[0]
    for s_id, dist in gauge_distance[g_id]:
        if dist<distance_threshold:
            print(s_id)
    break
