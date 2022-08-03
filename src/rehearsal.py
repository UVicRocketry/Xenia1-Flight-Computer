# Rehearsal script
#
# This script is meant to be run during the assembly rehearsal instead of main
# that will do the things with the sensors.
#
# MOST LOGIC SHOULD BE IN THE MAIN CODE. In theory, this should be only calling
# functions and controlling the flow.

import board
import math
import csv
import time
from airbrakes import Airbrakes
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_lsm9ds1
import adafruit_adxl34x
import RPi.GPIO as GPIO
import busio
from sensors.bme import Bme
from sensors.lsm import Lsm
from sensors.adx import Adx
from sensors.hx711s import Hx711
from flight_computer import FlightComputer as FC

i2c = board.I2C()

local_time = time.localtime()

lsm = None
adx = None
bme = None
flight_computer = None

def startup():
    """Initialize all the things"""
    global flight_computer
    flight_computer = FC()
    config_sensors()


def init_airbrakes():
    """This should initialize the airbrakes stepper motor and open and close airbrakes

    The main driver for the airbrakes should automatically do this upon
    initialization.

    Don't stand next to the airbrakes at this point.
    """
    airbrakes = Airbrakes(False, 8, 4, 7)
    # This will wave at the fans (move the brakes in and out)
    airbrakes.calibrate()
    airbrakes.deployBrakes(0)


def read_hx711s():
    """Basically like zeroing a scale, but with the strain gauges"""
    if strain_gauges.isReady():
        strain_gauges.readRaw()

def config_sensors():
    """Test readings from sensors, returns true if all sensors read something"""
    global bme
    global i2c
    global lsm
    global adx
    global strain_gauges

    lsm = Lsm(i2c)
    adx = Adx(i2c)
    bme = Bme(i2c)
    strain_gauges = Hx711()

    lsm.refresh()
    adx.refresh()
    bme.refresh()

    print("bme Temperature:", bme.temperature)
    print("Lsm Temperatrue:", lsm.temperature)
    print("Lsm Acceleration:", lsm.acceleration)
    print("Adx Acceleration:",  adx.acceleration)


def gather_data():
    """
    Collect data once and return. Data in blackbox will show up as a csv

    Order of collected data:
        Timestamp
        [bme]: temperature, humidity, pressure, altitude
        [lsm]: acceleration: x, y, z; magnometer: x, y, z; gyroscope: x, y, z, temperature
        [adx]: acceleration: x, y, z
    """
    global lsm
    global bme
    global adx

    lsm.refresh()
    bme.refresh()
    adx.refresh()

    lsm_acc_x, lsm_acc_y, lsm_acc_z = lsm.acceleration
    lsm_mag_x, lsm_mag_y, lsm_mag_z = lsm.magnetic
    lsm_gyro_x, lsm_gyro_y, lsm_gyro_z = lsm.gyro
    lsm_temp = lsm.temperature

    bme_temp = bme.temperature
    bme_alt = bme.altitude
    bme_hum = bme.humidity
    bme_press = bme.pressure

    adx_acc_x, adx_acc_y, adx_acc_z = adx.acceleration
    timestamp = time.strftime("%H:%M,%S", local_time)

    return [
        timestamp,
        bme_temp,
        bme_hum,
        bme_press,
        bme_alt,
        lsm_acc_x,
        lsm_acc_y,
        lsm_acc_z,
        lsm_mag_x,
        lsm_mag_y,
        lsm_mag_z,
        lsm_gyro_x,
        lsm_gyro_y,
        lsm_gyro_z,
        lsm_temp,
        adx_acc_x,
        adx_acc_y,
        adx_acc_z
    ]

def send_to_black_box(data, f):
    writer = csv.writer(f)
    writer.writerow(data)


def rehearsal():
    global flight_computer
    startup()
    # one minute of reading
    time_out = time.time() + 60
    f = open('/media/pi/XENIA-1_BB/rehearsal.txt', 'a')
    send_to_black_box("Here is the order of values: \n timestamp, bme_temp, bme_hum, bme_press, bme_alt, lsm_acc_x, lsm_acc_y, lsm_acc_z, lsm_mag_x, lsm_mag_y, lsm_mag_z, lsm_gyro_x, lsm_gyro_y, lsm_gyro_z, lsm_temp, adx_acc_x, adx_acc_y, adx_acc_z \n\n", f)
    while True:
        if time.time() > time_out:
            break
        data = gather_data()
        send_to_black_box(data, f)

    f.close()

    flight_computer.beep()
    flight_computer.beep()

if __name__ == "__main__":
    rehearsal()
