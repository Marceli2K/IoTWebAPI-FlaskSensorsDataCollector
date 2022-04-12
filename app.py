"""
app.py
"""
import os
import sqlite3
import sqlite3 as db
import pytz
from flask import Flask, render_template, send_from_directory, flash, app
from waitress import serve
from datetime import datetime


if not os.path.isfile('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE data (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        API_key text,
        date_time text,
        mac text,
        name text,
        lastname text,
        speed integer,
        localisation text,
        pulse integer,
        field integer,
        data real
        )""")
    conn.commit()
    conn.close()

def create_app():
    _APP = Flask(__name__)
    return _APP


APP = create_app()

@APP.route('/favicon.ico')
def favicon():
    """
    function to properly handle favicon
    :return:
    """
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@APP.route('/', methods=['GET'])
def main():
    """
    the main route rendering index.html
    :return:
    """




    conn = db.connect('data.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    pulse = c.execute('SELECT pulse FROM data').fetchall()
    labels = c.execute("SELECT date_time FROM data").fetchall()
    speed = c.execute('SELECT speed FROM data').fetchall()
    localisation = c.execute('SELECT localisation FROM data').fetchall()

    print(localisation)
    return render_template('index.html', template_labels=labels,
                           template_values_confirmed=pulse,
                           template_values_deaths=speed,
                           template_values_recovered=0)


@APP.route('/<string:item>', methods=['GET'])
def get_item_details(item):
    """
    the route for each "drilldown" item details
    :param item:
    :return:
    """
    filtered_data_set = 0

    return render_template('details.html', template_data_set=filtered_data_set)

API_KEY = "jp2gmd"
MAC_ADDRESS = "jp2gmd"
@APP.route("/update/API_key=<api_key>/mac=<mac>/name=<name>/lastname=<lastname>/speed=<speed>/localisation=<localisation>/pulse=<pulse>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(api_key, mac, name, lastname, speed, localisation, pulse, field, data):
    print("xd")
    if (api_key == API_KEY and mac == MAC_ADDRESS):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = datetime.now().strftime('%Y:%M:%D:%H:%M:%S.%f')[:-7]
        date_time_str = t
        c.execute("INSERT INTO data VALUES(:Id, :API_key, :date_time, :mac, :name, :lastname, :speed, :localisation, :pulse, :field, :data)",
                  {'Id': None, 'API_key': api_key, 'date_time': date_time_str, 'mac': mac, 'name' : name, 'lastname' : lastname, 'speed' : speed, 'localisation' : localisation, 'pulse' : pulse, 'field': int(field),
                   'data': round(float(data), 4)})
        conn.commit()
        c.close()
        conn.close()

        return render_template("update.html", data=data)

    else:
        return render_template("403.html")



if __name__ == "__main__":
    serve(APP, host='0.0.0.0', port=80, threads=4)
