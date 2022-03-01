#!/usr/bin/env python

from time import sleep
from unittest.mock import Mock
import random

# research needed
# Reading input
# have to install library on pi


class GeneralLSMObject :

    data={
        'a': float,
        'b': float,
        'c': float
    }
    


class GPIOReader():
    def __initializeRandomLSMObject(self):
        lsmobject = [random.uniform(0,100),random.uniform(0,100),random.uniform(0,100)]
        return lsmobject

    def __readBME280(self):
        ## TODO: Store Values in CSV file for external use ##
        print("Temperature: %0.1f C" % self.__bme280.temperature)
        print("Humidity: %0.1f %%" % self.__bme280.humidity)
        print("Pressure: %0.1f hPa" % self.__bme280.pressure)

    
    def __readLSM9DS1(self):
        ## TODO: Store Values in CSV file for external use ##
        print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Acceleration))
        print("Magnetometer (gauss: ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Magnetometer))
        print("Gyroscope (degrees/sec): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Gyroscope))
        print("Temperature: {0:0.3f}".format(self.__lsm9ds1.Temperature))


    # Private Method for setting up variables and inputs on pins
    def __setup(self):

        print("Initializing Board Setup.....")

        i2c = board.I2C() ## Uses board.SCL and board.SDA

        ## SETUP BME 280 SENSOR
        __bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        __lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

    
    ## Public Method to be called externally to grab data from sensors
    def retrieveData(self):
        self.__readBME280()
        self.__readLSM9DS1()


    def __init__(self, test):
        if test:
            self.__bme280 = Mock(temperature = random.uniform(-40,100),humidity = random.uniform(0,100), pressure = random.uniform(0,1000))
            lsm = self.__initializeRandomLSMObject()
            self.__lsm9ds1 = Mock(Acceleration = lsm, Magnetometer = lsm, Gyroscope = lsm, Temperature = random.uniform(0,100))
        else:
        ## INITIALIZE PINS
            self.__bme280 = None
            self.__lsm9ds1 = None
            self.setup()

    
    
