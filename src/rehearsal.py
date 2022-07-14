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

from HX711Multi import HX711_Multi

i2c = board.I2C()
# i2c = busio.I2C(board.SCL, board.SDA)

local_time = time.localtime()

#lsm = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
#bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#adx = adafruit_adxl34x.ADXL345(i2c)

# strain_gauges = HX711_Multi([11, 13, 15, 19, 21, 23, 29, 31, 33, 35, 37], 18, 128, False)

#bme.sea_level_pressure = 1011.9# 1013.25

def startup():
    """Initialize all the things"""
    init_stepper()
    
    config_buzzer()
    if config_sensors():
        beep()
    else:
        # didnt read all sensors not ready to go
        beep()
        time.sleep(0.2)
        beep()


def init_stepper():
    """This should initialize the airbrakes stepper motor and open and close airbrakes

    The main driver for the airbrakes should automatically do this upon
    initialization.

    Don't stand next to the airbrakes at this point."""

    # TODO: I have ZERO idea what this direction should be. There is a 50%
    #       chance that this is correct.
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    airbrakes = Airbrakes(direction = True)
    print("hello")

    GPIO.output(18, GPIO.LOW)
    GPIO.output(4, GPIO.HIGH)
    # This will wave at the fans (move the brakes in and out)
    airbrakes.calibrate()
    print("calibrate")
    


def read_hx711s():
    """Basically like zeroing a scale, but with the strain gauges"""
    if strain_gauges.isReady():
        strain_gauges.readRaw()


def config_buzzer():
    # GPIO.setmode(GPIO.BOARD)
    # Set the pins as outputs
    GPIO.setup(19, GPIO.OUT)

def beep():
    """This method should buzz the buzzer to let the operator know that setup
    is complete."""
    
    GPIO.output(19, GPIO.HIGH)
    
    
    print("beep")


def config_sensors():
    """Test readings from sensors, returns true if all sensors read something"""
    return True

def gather_data():
    """
    Collect data once and return. Data in blackbox will show up as a csv

    Order of collected data:
        Timestamp
        [bme]: temperature, humidity, pressure, altitude
        [lsm]: acceleration: x, y, z; magnometer: x, y, z; gyroscope: x, y, z, temperature
        [adx]: acceleration: x, y, z
    """

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

def send_to_blackbox(data):
    f = open('/media/pi/S4-4456/RocketData.txt', 'a')
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()


def rehearsal():
#      startup()

   # send_to_blackbox('Each line represents a reading')
   # send_to_blackbox('timestamp, bme_temperature, bme_humidity, bme_pressure, bme_altitude, lsm_acceleration_x, lsm_acceleration_y, lsm_acceleration_z, lsm_magnometer_x, lsm_magnometer_y, lsm_magnometer_z, bme_temperature, bme_altitude, adx_acceleration_x, adx_acceleration_y, adx_acceleration_z')
    config_buzzer()
    beep()
    
    start_up_time = time.strftime("%H:%M,%S", local_time)
    current_time = start_up_time
"""
    while True:
        current_time = time.strftime("%H:%M,%S", local_time)
        data = gather_data()
        send_to_blackbox(data)
        """

if __name__ == "__main__":
    rehearsal() # lol
