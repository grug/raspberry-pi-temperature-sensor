#!/usr/bin/env python
import os
import csv
import time
import datetime


def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20


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


def loop(ds18b20):
    while True:
        if read(ds18b20) != None:
            print("Current temperature : %0.3f C" % read(ds18b20)[0])


def kill():
    quit()


def write_to_file(reading):
    filename = time.strftime("%Y_%m_%d")

    with open('./data/{}.csv'.format(filename), mode='a') as csv_file:
        fieldnames = ['date', 'temperature']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {'date': datetime.datetime.now().isoformat(), 'temperature': reading})


if __name__ == '__main__':
    try:
        # serialNum = sensor()
        # reading = read(serialNum)
        write_to_file(5)
    except KeyboardInterrupt:
        kill()
