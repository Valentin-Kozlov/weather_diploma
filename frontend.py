from flask import Flask, render_template
import mariadb
import sys


def sorted_ends(s):
    res_find = s.find('_', 5)
    res = int(s[res_find+1:])
    return res


app = Flask(__name__)

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

cur = conn.cursor()

@app.route('/')
def dates():
    cur.execute('SHOW TABLES')
    result_tables = sorted([date[0] for date in cur.fetchall()], key=sorted_ends)
    return render_template('date.html', result_tables = result_tables)

@app.route('/<date>')
def table_date(date):
    cur.execute(f'SELECT * FROM {date}')
    result = cur.fetchall()
    date_form = date.replace('_', '.').split('.')
    date_form.reverse()
    date = '.'.join(date_form)
    return render_template('table_date.html', result = result, date = date)


if __name__ == '__main__':
    app.run()