#!/usr/bin/python3

from flask import Flask, send_file, make_response, render_template
import datetime
import io
from tinydb import TinyDB, Query
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time

app = Flask(__name__)

@app.route('/')
def main():
    temp = str(float(open("/sys/bus/i2c/devices/1-005c/temp1_input", "r").read())/10)
    hum = str(float(open("/sys/bus/i2c/devices/1-005c/humidity1_input", "r").read())/10)

    return render_template("sensors.html", title="Sensors", temp_data=temp, hum_data=hum)

@app.route('/images/<datatype>')
def images(datatype):
    db = TinyDB("sensor_log.json")
    Data = Query()
    data = db.search(Data.type == datatype)
    times = [datetime.datetime.strptime(i[1]['time'], "%Y-%m-%d %H:%M:%S") for i in enumerate(data)]
    datas = [i[1]['value'] for i in enumerate(data)]

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot_date(times, datas, '-')
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H:%M"))
    ax.xaxis.set_minor_locator(HourLocator())
    ax.autoscale_view()
    ax.grid(True)

    fig.autofmt_xdate()
    
    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    fig.savefig(png_output, format='png')
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == "__main__":
    app.run()
