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


from HX711Multi import HX711_Multi

i2c = board.I2C()
# i2c = busio.I2C(board.SCL, board.SDA)

local_time = time.localtime()

lsm = None
adx = None
bme = None

#lsm = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
#bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#adx = adafruit_adxl34x.ADXL345(i2c)

# strain_gauges = HX711_Multi([11, 13, 15, 19, 21, 23, 29, 31, 33, 35, 37], 18, 128, False)

#bme.sea_level_pressure = 1011.9# 1013.25

def startup():
    """Initialize all the things"""
    # init_airbrakes() 
    config_buzzer()
    
    
    if config_sensors():
        beep()
    else:
        # didnt read all sensors not ready to go
        beep()
        time.sleep(0.2)
        beep()


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


def config_buzzer():
    # GPIO.setmode(GPIO.BOARD)
    # Set the pins as outputs
    GPIO.setup(21, GPIO.OUT)

def beep():
    """This method should buzz the buzzer to let the operator know that setup
    is complete."""
    
    GPIO.output(21, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(21, GPIO.LOW)

    print("beep")


def failed_beep():
    GPIO.output(21, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(21, GPIO.LOW)

    print("beep :(")



def config_sensors():
    """Test readings from sensors, returns true if all sensors read something"""
    global bme
    global i2c
    global lsm
    global adx

    lsm = Lsm(i2c)
    adx = Adx(i2c)
    bme = Bme(i2c)
    
    lsm.refresh()
    adx.refresh()
    bme.refresh()
    
    print("bme Temperature:", bme.temperature)
    print("Lsm Temperatrue:", lsm.temperature)
    print("Lsm Acceleration:", lsm.acceleration)
    print("Adx Acceleration:",  adx.acceleration)
    
    return {
        bme.temperature and 
        lsm.temperature and 
        adx.acceleration
    }

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

def send_to_blackbox(data):
    writer = csv.writer(f)
    writer.writerow(data)


def rehearsal():
#      startup()

   # send_to_blackbox('Each line represents a reading')
   # send_to_blackbox('timestamp, bme_temperature, bme_humidity, bme_pressure, bme_altitude, lsm_acceleration_x, lsm_acceleration_y, lsm_acceleration_z, lsm_magnometer_x, lsm_magnometer_y, lsm_magnometer_z, bme_temperature, bme_altitude, adx_acceleration_x, adx_acceleration_y, adx_acceleration_z')
    #init_airbrakes()
    #config_buzzer()
    #beep()
    #time.sleep(0.1)

    startup()
    
    start_up_time = time.strftime("%H:%M,%S", local_time)
    current_time = start_up_time
    f = open('/media/pi/XENIA-1_BB/rehearsal.txt', 'a')
"""
    while True:
        current_time = time.strftime("%H:%M,%S", local_time)
        data = gather_data()
        send_to_blackbox(data)
        """
    f.close()

if __name__ == "__main__":
    rehearsal() # lol
