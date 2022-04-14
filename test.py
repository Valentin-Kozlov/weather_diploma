import mariadb
import sys

# connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="172.17.145.200",
        port=3306,
        database="test"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
    
    
cur = conn.cursor()

# cur.execute(f'''CREATE TABLE test(id VARCHAR(20), weather_state_name VARCHAR(20),
#                 wind_direction_compass VARCHAR(20), created VARCHAR(40), applicable_date VARCHAR(20),
#                 min_temp VARCHAR(20), max_temp VARCHAR(20), the_temp VARCHAR(20))''')

id = 'id1'
weather_state_name = 'weather_state_name2'
wind_direction_compass = 'wind3'
created = 'created4'
applicable_date = 'applicable_date5'
min_temp = '8887'
max_temp = 'max_temp7'
the_temp = 'the_temp8'

cur.execute(f'''UPDATE test SET
            weather_state_name='{weather_state_name}',
            wind_direction_compass='{wind_direction_compass}',
            created='{created}',
            applicable_date='{applicable_date}',
            min_temp='{min_temp}',
            the_temp='{the_temp}' WHERE id='{id}'
            ''')


# cur.execute(f'''INSERT INTO test (id, weather_state_name,
#                             wind_direction_compass, created, applicable_date, min_temp,
#                             max_temp, the_temp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (id,
#                             weather_state_name, wind_direction_compass,
#                             created, applicable_date, min_temp,
#                             max_temp, the_temp))
conn.commit();
