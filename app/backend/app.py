from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import mariadb
import os
import requests
import calendar
import json
import time
from datetime import date, timedelta
from operator import itemgetter
from prometheus_flask_exporter import PrometheusMetrics

flask_user = os.getenv('username_db')
flask_password = os.getenv('password_db')
flask_db = os.getenv('name_service_db')
flask_database = os.getenv('database')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= f"mysql+mysqldb://{flask_user}:{flask_password}@{flask_db}:3306/{flask_database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

metrics = PrometheusMetrics(app, path=None)
metrics.start_http_server(8000)


conn = mariadb.connect(
    user=flask_user,
    password=flask_password,
    host=flask_db,
    port=3306,
    database=flask_database
    )
cur = conn.cursor()


def sorted_ends(s):
    res_find = s.find('.', 0)
    res = int(s[res_find+1:])
    return res


list_current_date = list(map(int, str(date.today()).split('-')))
count_days_month = calendar.monthrange(list_current_date[0], list_current_date[1])[1]
today = list_current_date[2]

if int(today) + 5 > int(count_days_month):
    ends_range = count_days_month + 1
else:
    ends_range = int(today) + 5
    
names_table = [f'{list_current_date[0]}_{list_current_date[1]}_{day}' for day in range(1,ends_range)]


def class_db(db, names_table):
    for name in names_table:
        cur.execute(f"SHOW TABLES LIKE '{name}'")
        try: 
            if name not in cur.fetchall()[0]:
                class date_tables(db.Model):
                    __tablename__ = name
                    id = db.Column(db.String(20), primary_key=True) 
                    weather_state_name = db.Column(db.String(20), nullable=True)
                    wind_direction_compass = db.Column(db.String(20), nullable=True) 
                    created = db.Column(db.String(40), nullable=True) 
                    applicable_date = db.Column(db.DateTime(20), nullable=False)
                    min_temp = db.Column(db.String(20), nullable=True) 
                    max_temp = db.Column(db.String(20), nullable=True) 
                    the_temp = db.Column(db.String(20), nullable=True)
            else:
                continue  
        except IndexError:
                class date_tables(db.Model):
                    __tablename__ = name
                    id = db.Column(db.String(20), primary_key=True) 
                    weather_state_name = db.Column(db.String(20), nullable=True)
                    wind_direction_compass = db.Column(db.String(20), nullable=True) 
                    created = db.Column(db.String(40), nullable=True) 
                    applicable_date = db.Column(db.DateTime(20), nullable=False)
                    min_temp = db.Column(db.String(20), nullable=True) 
                    max_temp = db.Column(db.String(20), nullable=True) 
                    the_temp = db.Column(db.String(20), nullable=True)
    db.create_all()


def update_database(names_table, conn, cur):
    # check and delete old tables in database
    cur.execute('SHOW TABLES')
    table_in_database = {table[0]:0 for table in cur.fetchall()}
    for table_key in table_in_database.keys():
        if table_key in names_table:
            table_in_database[table_key] = 1
        else:
            cur.execute(f'DROP TABLE {table_key}')
    for name in names_table:        
        name_for_get = name.replace('_', '/')
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
                continue


class_db(db, names_table)
# update_database(names_table, conn, cur)


@app.route('/api/name_tables')
def table_dates():
    cur.execute('SHOW TABLES')
    result_tables = sorted([date[0] for date in cur.fetchall()], key=sorted_ends)
    json_res = json.dumps(result_tables)
    return json_res


@app.route('/api/<date>')
def table_of_date(date):
    cur.execute(f'SELECT * FROM {date}')
    result = json.dumps(cur.fetchall(), indent=4, sort_keys=True, default=str)
    return result


@app.route('/api/update')
def update():
    start_time = time.monotonic()
    class_db(db, names_table)
    update_database(names_table, conn, cur)
    end_time = time.monotonic()
    count_time = timedelta(seconds=end_time - start_time)
    json_res = json.dumps(count_time, indent=4, sort_keys=True, default=str)
    return json_res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)