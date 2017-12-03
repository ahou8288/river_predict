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


def process_dates(data):
    return [(datetime.date(i[0], i[1], i[2]), i[3]) for i in data]


levels = process_dates(levels)
rain = process_dates(rain)


def find_gaps(data):
    subsection = 1
    gaps = []
    sections = []
    for i in range(len(data) - 1):
        today = data[i][0]
        tomorrow = data[i + 1][0]
        gap = (tomorrow - today).days
        subsection += 1
        if gap > 1:
            sections.append(subsection)
            subsection = 0
            gaps.append(gap)
    sections.append(subsection)
    return (gaps, sections)
    # return (sorted(gaps),sorted(sections))
# rain_gaps, rain_sections = find_gaps(rain)
# levels_gaps, levels_sections = find_gaps(levels)

# print('start and end of dates')
# start = min(levels[0][0], rain[0][0]).toordinal()
start = 698222
# end = max(levels[-1][0], rain[-1][0]).toordinal()
end = 736555

for i in range(start,end+1):
    print(i)
