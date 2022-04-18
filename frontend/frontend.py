from flask import Flask, render_template
import os
import requests

address_back = '127.0.0.1:3000'


app = Flask(__name__)


@app.route('/', methods=['GET'])
def dates():
    name_table = requests.get(f'http://{address_back}/api/name_tables').json()
    return render_template('date.html', result_tables = name_table)

@app.route('/<date>', methods=['GET'])
def table_date(date):
    table = requests.get(f'http://{address_back}/api/{date}').json()
    date_form = date.replace('_', '.').split('.')
    date_form.reverse()
    date = '.'.join(date_form)
    return render_template('table_date.html', result = table, date = date)

@app.route('/update', methods=['GET'])
def update():
    update = requests.get(f'http://{address_back}/api/update').json()
    return 'ok'


if __name__ == '__main__':
    app.run()