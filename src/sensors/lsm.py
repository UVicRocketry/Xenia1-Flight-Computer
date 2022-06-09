import adafruit_lsm9ds1
import board

class Lsm:

    __lsm9ds1 = None

    __gyroscope = None
    __magnetometer = None
    __acceleration = None
    __temperature = None

    def __init__(self):
        i2c = board.I2C()
        self.__lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        # TODO: initialize pins (from wiring diagram)


    def read_temperature(self):
        """Safety first"""
        return self.read_temperature_unsafe() or self.__temperature

    def read_temperature_unsafe(self):
        try:
            self.__temperature = self.__lsm9ds1.acceleration
            return self.__temperature
        except:
            return None

    def read_acceleration(self):
        return self.__read_acceleration_unsafe() or self.__acceleration

    def __read_acceleration_unsafe(self):
        try:
            self.__acceleration = self.__lsm9ds1.acceleration
            return self.__acceleration
        except:
            return None

    def read_magnetometer(self):
        return self.__read_magnetometer_unsafe() or self.__magnetometer

    def __read_magnetometer_unsafe(self):
        try:
            self.__magnetometer = self.__lsm9ds1.magnetometer
            return self.__magnetometer
        except:
            return None

    def read_gyroscope(self):
        return self.__read_gyroscope_unsafe() or self.__gyroscope

    def __read_gyroscope_unsafe(self):
        try:
            self.__gyroscope = self.__lsm9ds1.gyroscope
            return self.__gyroscope
        except:
            return None