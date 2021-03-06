#!/usr/bin/env python
import os
import csv
import time
import datetime


def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    return celsius


def write_to_file(reading, probe):
    filename = time.strftime("%Y_%m_%d")

    with open('./data/{}-{}.csv'.format(filename, probe), mode='a') as csv_file:
        fieldnames = ['date', 'temperature']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {'date': datetime.datetime.now().isoformat(), 'temperature': reading})


if __name__ == '__main__':
    try:
        water_shallow = read('28-011450496aaa')
        air = read('28-01145026caaa')
        water_deep = read('28-011929d17635')
        write_to_file(water_shallow, 'water_shallow')
        write_to_file(air, 'air')
        write_to_file(water_deep, 'water_deep')
    except KeyboardInterrupt:
        quit()
