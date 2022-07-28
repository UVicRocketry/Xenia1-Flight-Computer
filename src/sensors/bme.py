from adafruit_bme280 import basic as adafruit_bme280
import numpy as np


# TODO: update sea level before final launch
SEA_LEVEL_PRESSURE = 1013.25

class Bme:
    """
    bme sensor object

    ...

    Attributes
    ----------

    __bme280 : object
        Bme driver for the bme sensor, holds methods to
        get each sensor value

    __temperature : float
        Temperature reading from the bme

    __humidity : (tuple)
        Moistness of from the reading bme

    __pressure : tuple
        pressure reading form the bme

    __altitude : tuple
        altitude reading from the bme

    Methods
    -------

    refresh():
        reads new values from all sensors on chip and stores the data.

    @property getters:
        Returns the latest value stored in the variable.

    __read_/.../():
        Reads the sensor and returns sensor value or None if read was unsuccessful

    """
    
    INPUT_FILEPATH = './test.csv'

    __bme280 = None

    __temperature = None
    __humidity = None
    __pressure = None
    __altitude = None
    __input_file = None
    __input_array = None
    __y_index = 0


    def __init__(self, i2c):
        try:
            self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
            self.__bme280.sea_level_pressure = SEA_LEVEL_PRESSURE
            self.__input_file = open(INPUT_FILEPATH)
            self.__input_array = np.loadtxt(self.__input_file)
        except ValueError:
            self.__bme280 = {
                'pressure': 0,
                'temperature': 0,
                'humidity': 0,
                'altitude': 0
            }

    def refresh(self):
        try:
            self.__humidity = self.__input_array[0][self.__y_index]
            self.__pressure = self.__input_array[1][self.__y_index]
            self.__temperature = self.__input_array[2][self.__y_index]
            self.__altitude = self.__input_array[3][self.__y_index]
            self.__y_index = self.__y_index + 1
        except:
            self.__humidity = None
            self.__pressure = None
            self.__temperature = None
            self.__altitude = None


    @property
    def humidity(self):
        return self.__humidity


    def __read_humidity(self):
        try:
            return self.__bme280.humidity
        except:
            return None


    @property
    def pressure(self):
        return self.__pressure


    def __read_pressure(self):
        try:
            return self.__bme280.pressure
        except:
            return None


    @property
    def temperature(self):
        return self.__temperature


    def __read_temperature(self):
        try:
            return self.__bme280.temperature
        except:
            return None


    @property
    def altitude(self):
        return self.__altitude()


    def __read_altitude(self):
        try:
            return self.__bme280.altitude
        except:
            return None
