# Database
import sqlite3
# import csv
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
# start = max(levels[0][0], rain[0][0]).toordinal()
start = 714216
# end = min(levels[-1][0], rain[-1][0]).toordinal()
end = 736543


def dates_to_dict(data):
    output = {}
    for i in data:
        output[i[0].toordinal()] = i[1]
    return output

rain_dict = dates_to_dict(rain)
levels_dict = dates_to_dict(levels)

output = []
graph_data_x = []
graph_data_y1 = []
graph_data_y2 = []
for i in range(start, end + 1):
    # print(i)
    today = datetime.datetime.fromordinal(i)
    today_rain = 'NaN'
    if i in rain_dict.keys():
        today_rain = rain_dict[i]
    today_levels = 'NaN'
    if i in levels_dict:
        today_levels = levels_dict[i]
    today_data = [
        '{}-{}-{}'.format(today.year, today.month, today.day),
        str(today_rain),
        str(today_levels)]
    graph_data_x.append(i-start)
    graph_data_y1.append(today_levels)
    graph_data_y2.append(today_rain)
    output.append(today_data)

# print(output)
# f=open('nymbo.csv','w')
# f.write('\n'.join([','.join(i) for i in output]))


import matplotlib.pyplot as plt
#date stuff


#plotting stuff
fig, ax1 = plt.subplots()
plt.title("Nymboida")
ax1.set_xlabel('Date')
ax1.plot(graph_data_x,graph_data_y1,'b-')
ax1.tick_params('y', colors='b')
ax1.set_ylabel('Level (m)',color='b')

ax2=ax1.twinx()
ax2.plot(graph_data_x,graph_data_y2,'r-')
ax2.tick_params('y', colors='r')
ax2.set_ylabel('Daily Rainfall (mm)',color='r')

ax1.grid(True)

plt.show()