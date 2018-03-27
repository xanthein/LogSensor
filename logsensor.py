#!/usr/bin/python3

from tinydb import TinyDB
import time
import datetime

def main():
    db = TinyDB("sensor_log.json")
    temp_data = 0.0
    hum_data = 0.0

    for i in range(0, 10):
        temp_data += float(open("/sys/bus/i2c/devices/1-005c/temp1_input", "r").read())
        hum_data += float(open("/sys/bus/i2c/devices/1-005c/humidity1_input", "r").read())
        time.sleep(1)
    local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.insert({'time': local_time, 'type': 'temperature', 'value': temp_data/100})
    db.insert({'time': local_time, 'type': 'humidity', 'value': hum_data/100})

if __name__ == "__main__":
    main()
