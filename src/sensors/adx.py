import adafruit_adxl37x
from safe_value import SafeValue

"""
read_acceleration_safe(): reads new values from sensor and stores the data read in a SafeValue object. Returns the latest safe
value or the backup function if the sensor has not read values for longer than the TIMEOUT Specification foun in safe_value.py.
This function can be called to read new data from sensor and send data to calculations.

get_acceleration_unsafe(): returns the latest Sensor values even if they are of None type. Does NOT read new data from sensors.
This function can be called to send data to black box/ground station

__read_acceleration_unsafe(): Reads the sensor and returns None read was unsuccessful
"""


class Adx:
    __safe_value = SafeValue([-100,100],-9.8)

    __adxl375 = None

    __acceleration = None

    def __init__(self):
        self.__adxl375 = adafruit_adxl37x.ADXL375(i2c)
    
    def read_acceleration_safe(self):
        #gets new data from sensors and uses update() function in safe_value class to place data in last_value and last_safe_value
        self.__safe_value.update(self.__read_acceleration_unsafe())
        #returns last safe value or result of alternative function if the sensor has returned None for longer than the TIMEOUT setting.
        return self.__safe_value.get_last_safe_value()

    def get_acceleration_unsafe(self):
        #returns the last unsafe value but does not update object.
        return self.__safe_value.get_last_unsafe_value()

    def __read_acceleration_unsafe(self):
        try:
            self.__acceleration = self.__adxl375.acceleration
            return self.__acceleration
        except:
            return None
    

