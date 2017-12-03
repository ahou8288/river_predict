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

def find_gaps(data):
    subsection = 1
    gaps = []
    sections = []
    for i in range(len(data) - 1):
        today = datetime.date(data[i][0], data[i][1], data[i][2])
        tomorrow = datetime.date(data[i + 1][0], data[i + 1][1], data[i + 1][2])
        gap = (tomorrow - today).days
        subsection += 1
        if gap > 1:
            sections.append(subsection)
            subsection = 0
            gaps.append(gap)
    sections.append(subsection)
    return (gaps,sections)
    # return (sorted(gaps),sorted(sections))

rain_gaps,rain_sections = find_gaps(rain)
levels_gaps,levels_sections = find_gaps(levels)

print('len levels')
print(len(levels))
# print(sum(levels_sections))
print('len rain')
print(len(rain))
# print(sum(rain_sections))

print('rain_gaps')
print(rain_gaps)
print('rain_sections')
print(rain_sections)

print('levels_gaps')
print(levels_gaps)
print('levels_sections')
print(levels_sections)

