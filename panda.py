import sqlite3

conn = sqlite3.connect('mydb.db')
c = conn.cursor()


# c.execute('SELECT station_id, count(*) FROM rainfall GROUP BY station_id ORDER BY count(*)')
# rainfalls = c.fetchall()
# c.execute('SELECT gauge_id, count(*) FROM levels GROUP BY gauge_id ORDER BY count(*)')
# levels = c.fetchall()
# print(rainfalls)
# print(levels)

c.execute('select distinct gauge_id from levels')
station1 = set(c.fetchall())
c.execute('select id from gauges')
station2 = set(c.fetchall())
print(len(station1))
print(len(station2))
print(station1 - station2)

def load_df(table_name):
    import pandas
    print('Loading ' + table_name)
    query = 'SELECT * FROM ' + table_name
    df = pandas.read_sql_query(query, conn)
    return df


# levels = load_df('levels')
# gauges = load_df('gauges')
# stations = load_df('stations')
# rainfall = load_df('rainfall')

conn.close()

# print('Showing describe output')
# print(levels.describe())
# print(gauges.describe())
# print(stations.describe())
# print(rainfall.describe())
