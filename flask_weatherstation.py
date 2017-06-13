from flask import Flask
from flask import render_template
from Classes import Database_class
from Classes import time_local_time
import time
import datetime
import os

app = Flask(__name__)


@app.route('/')
def page_startup():
    return render_template("template_home.html")


@app.route('/home')
def page_home():
    return render_template("template_home.html")


@app.route('/air_quality')
def page_air_quality():
    database_weatherstation = Database_class.Database_class()
    hour_now = int(time_local_time.time_local_time().get_local_time()[0:2])
    lst_data = database_weatherstation.get_time_and_measurement_from_weatherstation(hour_now, 1)
    return render_template("template_air_quality.html", time=lst_data[0], values=lst_data[1])


@app.route('/humidity')
def page_humidity():
    database_weatherstation = Database_class.Database_class()
    hour_now = int(time_local_time.time_local_time().get_local_time()[0:2])
    lst_data = database_weatherstation.get_time_and_measurement_from_weatherstation(hour_now, 2)
    return render_template("template_humidity.html", time=lst_data[0], values=lst_data[1])


@app.route('/light')
def page_light():
    database_weatherstation = Database_class.Database_class()
    hour_now = int(time_local_time.time_local_time().get_local_time()[0:2])
    lst_data = database_weatherstation.get_time_and_measurement_from_weatherstation(hour_now, 3)
    return render_template("template_light.html", time=lst_data[0], values=lst_data[1])


@app.route('/temperature')
def page_temperature():
    database_weatherstation = Database_class.Database_class()
    hour_now = int(time_local_time.time_local_time().get_local_time()[0:2])
    lst_data = database_weatherstation.get_time_and_measurement_from_weatherstation(hour_now, 4)
    return render_template("template_temperature.html", time=lst_data[0], values=lst_data[1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=86, debug=True)
