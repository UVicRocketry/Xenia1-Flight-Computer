#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO
import board
from adafruit_bme280 import basic as adafruit_bme280

# research needed
# Reading input
# have to install library on pi
class GPIOReader():

    __bme280 = None

    def __readBME280(self):
        ## TODO: Store Values in CSV file for external use ##
        print("Temperature: %0.1f C" % __bme280.temperature)
        print("Humidity: %0.1f %%" % __bme280.humidity)
        print("Pressure: %0.1f hPa" % __bme280.pressure)
    

    ## Private Method for setting up variables and inputs on pins
    def __setup(self):

        print("Initializing Board Setup.....")

        i2c = board.I2C() ## Uses board.SCL and board.SDA

        ## SETUP BME 280 SENSOR
        __bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    ## Public Method to be called externally to grab data from sensors
    def retrieveData(self):
        __readBME280()


    def __init__(self):

        ## INITIALIZE PINS
        setup()

    
    
