# module Imports
import mariadb
import sys
import requests
import calendar
from datetime import date
from operator import itemgetter


# get current date
list_current_date = list(map(int, str(date.today()).split('-')))
count_days_month = calendar.monthrange(list_current_date[0], list_current_date[1])[1]
today = list_current_date[2]


# сделать проверку на текущую дату+5, чтобы не писать пустые дни из будущего
if int(today) + 5 > int(count_days_month):
    ends_range = count_days_month + 1
else:
    ends_range = int(today) + 5


# connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="192.168.146.162",
        port=3306,
        database="test"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# get Cursor
cur = conn.cursor()


# list of date for creating tables in database
names_table = [f'{list_current_date[0]}_{list_current_date[1]}_{day}' for day in range(1,ends_range)]


# check and delete old tables in database
cur.execute('SHOW TABLES')
table_in_database = {table[0]:0 for table in cur.fetchall()}
for table_key in table_in_database.keys():
    if table_key in names_table:
        table_in_database[table_key] = 1
    else:
        cur.execute(f'DROP TABLE {table_key}')


# create tables in database
for name in names_table:
    cur.execute(f'''CREATE TABLE if not exists {name}(id VARCHAR(20), weather_state_name VARCHAR(20),
                wind_direction_compass VARCHAR(20), created VARCHAR(40), applicable_date VARCHAR(20),
                min_temp VARCHAR(20), max_temp VARCHAR(20), the_temp VARCHAR(20))''')
    name_for_get = name.replace('_', '/')
    
    #api request from metaweather.com
    req = (requests.get(f'https://www.metaweather.com/api/location/44418/{name_for_get}')).json()
    req_sorted_by_created = sorted(req, key=itemgetter('created'))
    for data_line in req_sorted_by_created:
         try: 
             cur.execute(f'''INSERT INTO {name} (id, weather_state_name,
                            wind_direction_compass, created, applicable_date, min_temp,
                            max_temp, the_temp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (data_line['id'],\
                             data_line['weather_state_name'], data_line['wind_direction_compass'],\
                             data_line['created'], data_line['applicable_date'], data_line['min_temp'],\
                             data_line['max_temp'], data_line['the_temp']))
             conn.commit();
         except mariadb.Error as mariadb_error: 
             print("MariaDB error: " + str(mariadb_error))

             
# show tables
cur.execute('SHOW TABLES')
for table in cur:
    print(table)
