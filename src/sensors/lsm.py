import adafruit_lsm9ds1
import board
from safe_value import SafeValue

"""
read_/../_safe(): reads new values from sensor and stores the data read in a SafeValue object. Returns the latest safe
value or the backup function if the sensor has not read values for longer than the TIMEOUT Specification foun in safe_value.py.
This function can be called to read new data from sensor and send data to calculations.

get_/.../_unsafe(): returns the latest Sensor values even if they are of None type. Does NOT read new data from sensors.
This function can be called to send data to black box/ground station

__read_/.../_unsafe(): Reads the sensor and returns None read was unsuccessful
"""

class Lsm:

    __lsm9ds1 = None

    __gyroscope = None
    __gyroscope_safe_value = SafeValue([-100,100], 15)
    __magnetometer = None
    __magnetometer_safe_value = SafeValue([-100,100], 15)
    __acceleration = None
    __acceleration_safe_value = SafeValue([-100,100], 15)
    __temperature = None
    __temperature_safe_value = SafeValue([-100,100], 15)

    def __init__(self):
        i2c = board.I2C()
        self.__lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        # TODO: initialize pins (from wiring diagram)


    def read_temperature_safe(self):
        """Safety first"""
        self.__temperature_safe_value.update(self.__read_temperature_unsafe())
        return self.__temperature_safe_value.get_last_safe_value()

    def get_temperature_unsafe(self):
        return self.__temperature_safe_value.get_last_unsafe_value()

    def __read_temperature_unsafe(self):
        try:
            self.__temperature = self.__lsm9ds1.Temperature
            return self.__temperature
        except:
            return None

    def read_acceleration_safe(self):
        self.__acceleration_safe_value.update(self.__read_acceleration_unsafe())
        return self.__acceleration_safe_value.get_last_safe_value()

    def get_acceleration_unsafe(self):
        return self.__acceleration_safe_value.get_last_unsafe_value()

    def __read_acceleration_unsafe(self):
        try:
            self.__acceleration = self.__lsm9ds1.Acceleration
            return self.__acceleration
        except:
            return None

    def read_magnetometer_safe(self):
        self.__magnetometer_safe_value.update(self.__read_magnetometer_unsafe())
        return self.__magnetometer_safe_value.get_last_safe_value()

    def get_magnetometer_unsafe(self):
        return self.__magnetometer_safe_value.get_last_unsafe_value()

    def __read_magnetometer_unsafe(self):
        try:
            self.__magnetometer = self.__lsm9ds1.Magnetometer
            return self.__magnetometer
        except:
            return None

    def read_gyroscope_safe(self):
        self.__gyroscope_safe_value.update(self.__read_gyroscope_unsafe())
        return self.__gyroscope_safe_value.get_last_safe_value()

    def get_gyroscope_unsafe(self):
        return self.__gyroscope_safe_value.get_last_unsafe_value()

    def __read_gyroscope_unsafe(self):
        try:
            self.__gyroscope = self.__lsm9ds1.Gyroscope
            return self.__gyroscope
        except:
            return None