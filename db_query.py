
# Database
import sqlite3

conn = sqlite3.connect('mydb.db')
c = conn.cursor()

def display_table_info(table_name):
	print(table_name.upper())
	q = c.execute("select count(*) from "+table_name)
	print('Table has {} rows.'.format(q.fetchone()[0]))
	q = c.execute("select * from "+table_name+" LIMIT 1")
	print('The columns are; '+', '.join([i[0] for i in q.description]))
	print('The first row contains;\n{}\n'.format(q.fetchone()))

display_table_info('gauges')
display_table_info('stations')
display_table_info('rainfall')
display_table_info('levels')