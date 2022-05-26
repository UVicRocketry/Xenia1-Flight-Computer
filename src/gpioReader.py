from time import sleep
from unittest.mock import Mock
import random
import pytest
import board
import adafruit_lsm9ds1
from adafruit_bme280 import basic as adafruit_bme280

class GeneralLSMObject :

    data={
        'a': float,
        'b': float,
        'c': float
    }

#TODO: write issue to change from print statements to updating rocketData in main (make read functions return objects ...)
class GPIOReader():
    def __initializeRandomLSMObject(self):
        lsmobject = [random.uniform(0,100),random.uniform(0,100),random.uniform(0,100)]
        return lsmobject

    def __readBME280(self):
        return {
            'temperature' : self.__bme280.temperature,
            'humidity' : self.__bme280.humidity,
            'pressure' : self.__bme280.pressure
        }

    
    def __readLSM9DS1(self):
        print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Acceleration))
        print("Magnetometer (gauss: ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Magnetometer))
        print("Gyroscope (degrees/sec): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(*self.__lsm9ds1.Gyroscope))
        print("Temperature: {0:0.3f}".format(self.__lsm9ds1.Temperature))
        return {
            'acceleration' : 
        }


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


    def __init__(self, test, BMETemperature, BMEHumidity, BMEPressure, LSMAcceleration, LSMMagnetometer, LSMGyroscope, LSMTemperature):
        if test and not (BMETemperature or BMEHumidity or BMEPressure or LSMAcceleration or LSMMagnetometer or LSMGyroscope or LSMTemperature):
            #Generalized test mode is activated. Random numbers will be generated for BME and LSM sensors and program will run on a loop.
            self.__bme280 = Mock(temperature = random.uniform(-40,100),humidity = random.uniform(0,100), pressure = random.uniform(0,1000))
            lsm = self.__initializeRandomLSMObject()
            self.__lsm9ds1 = Mock(Acceleration = lsm, Magnetometer = lsm, Gyroscope = lsm, Temperature = random.uniform(0,100))
        elif test:
            #Pytest test mode is activated. A single function will be tested using specific input.
            self.__bme280 = Mock(temperature = BMETemperature, humidity = BMEHumidity, pressure = BMEPressure)
            self.__lsm9ds1 = Mock(Acceleration = LSMAcceleration, Magnetometer = LSMMagnetometer, Gyroscope = LSMGyroscope, Temperature = LSMTemperature)
        else:
        ## INITIALIZE PINS
            self.__bme280 = None
            self.__lsm9ds1 = None
            self.__setup()

