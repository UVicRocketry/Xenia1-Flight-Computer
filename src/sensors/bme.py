import board
from adafruit_bme280 import basic as adafruit_bme280

"""
read_/../_safe(): reads new values from sensor and stores the data read in a SafeValue object. Returns the latest safe
value or the backup function if the sensor has not read values for longer than the TIMEOUT Specification foun in safe_value.py.
This function can be called to read new data from sensor and send data to calculations.

get_/.../_unsafe(): returns the latest Sensor values even if they are of None type. Does NOT read new data from sensors.
This function can be called to send data to black box/ground station

__read_/.../_unsafe(): Reads the sensor and returns None read was unsuccessful
"""

class Bme: 

    __bme280 = None

    __temperature = None
    __humidity = None
    __pressure = None

    def __init__(self):
        i2c = board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self.__bme280.sea_level_pressure = 1013.25
        # the datasheet lists this as a generic value, but we should get an accurate one before launch

    
    def read_humidity_safe(self):
        #read humidity and store in safe value
        self.__humidity_safe_value.update(self.__read_humidity_unsafe)
        #return last safe value from SafeValue Object
        return self.__humidity_safe_value.get_last_safe_value()

    def get_humidity_unsafe(self):
        #returns last value from SafeValue object for Black Box data
        return self.__humidity_safe_value.get_last_unsafe_value()

    def __read_humidity_unsafe(self): 
        try: 
            self.__humidity = self.__bme280.humidity
            return self.__humidity
        except:
            return None
    
    def read_pressure_safe(self):
        #read pressure and store in safe value
        self.__pressure_safe_value.update(self.__read_pressure_unsafe)
        #return last safe value from SafeValue Object
        return self.__pressure_safe_value.get_last_safe_value()

    def get_pressure_unsafe(self):
        return self.__pressure_safe_value.get_last_unsafe_value()
    
    def __read_pressure_unsafe(self): 
        try: 
            self.__pressure = self.__bme280.pressure
            return self.__pressure
        except:
            return None

    def read_temperature_safe(self):
        #read temperature and store in safe value
        self.__temperature_safe_value.update(self.__read_temperature_unsafe)
        #return last safe value from SafeValue Object
        return self.__temperature_safe_value.get_last_safe_value()

    def get_temperature_unsafe(self):
        #return unsafe value for black box
        return self.__temperature_safe_value.get_last_unsafe_value()

    def __read_temperature_unsafe(self):
        #attempt to read sensor and return None if unsuccessful
        try: 
            self.__temperature = self.__bme280.temperature
            return self.__temperature
        except:
            return None
