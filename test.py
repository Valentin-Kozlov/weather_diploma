import mariadb
import sys
import mariadb
import sys
import requests
import calendar
from datetime import date
from operator import itemgetter

# connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="flask",
        password="flaskpass",
        host="192.168.146.162",
        port=3306,
        database="test_flask"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
    
cur = conn.cursor()    

list_current_date = list(map(int, str(date.today()).split('-')))
count_days_month = calendar.monthrange(list_current_date[0], list_current_date[1])[1]
today = list_current_date[2]

if int(today) + 5 > int(count_days_month):
    ends_range = count_days_month + 1
else:
    ends_range = int(today) + 5
    
names_table = [f'{list_current_date[0]}_{list_current_date[1]}_{day}' for day in range(1,ends_range)]


# for i in names_table:
#     cur.execute(f"SHOW TABLES LIKE '{i}'")
#     print(cur.fetchall())
#     if cur.fetchall() == 0:
#         print('yes')
    # if i in cur.fetchall()[0]:
    #     print('yes')
    # else:
    #     print('no')


for name in names_table: 
    cur.execute(f'DROP TABLE {name}')

conn.commit();
