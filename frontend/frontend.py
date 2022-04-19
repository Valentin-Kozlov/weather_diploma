from flask import Flask, render_template, send_from_directory
import os
import requests

# address_back = '127.0.0.1:3000'
# address_back = os.environ('ADDRESS_BACK') 
address_back = 'backend-diploma:3000'


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

@app.route('/update')
def update():
    time = requests.get(f'http://{address_back}/api/update').json()
    return render_template('update.html', time=time)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()