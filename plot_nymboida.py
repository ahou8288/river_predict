# Database
import sqlite3
import csv
import datetime


def sql(query):
    c.execute(query)
    return c.fetchall()

conn = sqlite3.connect('mydb.db')
c = conn.cursor()

nymbo_gauge = 204001
nymbo_station = 58045

rain = sql('''
    SELECT year, month, day, rainfall
    FROM rainfall
    WHERE station_id = {}
    ORDER BY year,month,day
    '''.format(nymbo_station))
levels = sql('''
    SELECT year, month, day, level
    FROM levels
    WHERE gauge_id = {}
    ORDER BY year,month,day
    '''.format(nymbo_gauge))

subsection = 0
gaps = []
sections = []
for i in range(len(rain) - 1):
    today = datetime.date(rain[i][0], rain[i][1], rain[i][2])
    tomorrow = datetime.date(rain[i + 1][0], rain[i + 1][1], rain[i + 1][2])
    subsection += 1
    gap = (tomorrow - today).days
    if gap > 1:
        sections.append(subsection)
        subsection = 0
        gaps.append(gap)

print(sorted(gaps))
print(sorted(sections))
# print(len(rain))
# print(len(levels))
