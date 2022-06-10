import adafruit_lsm9ds1
import board

class Lsm:

    __lsm9ds1 = None

    gyroscope = None
    magnetometer = None
    acceleration = None
    temperature = None

    def __init__(self):
        i2c = board.I2C()
        self.__lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        # TODO: initialize pins (from wiring diagram)

    @property
    def temperature(self):
        """Safety first"""
        return self.read_temperature_unsafe() or self.temperature

    def read_temperature_unsafe(self):
        try:
            self.temperature = self.__lsm9ds1.temperature
            return self.temperature
        except:
            return None

    def acceleration(self):
        return self.__read_acceleration_unsafe() or self.acceleration

    def __read_acceleration_unsafe(self):
        try:
            self.acceleration = self.__lsm9ds1.acceleration
            return self.acceleration
        except:
            return None
    
    @property
    def magnetometer(self):
        return self.__read_magnetometer_unsafe() or self.magnetometer

    def __read_magnetometer_unsafe(self):
        try:
            self.magnetometer = self.__lsm9ds1.magnetometer
            return self.magnetometer
        except:
            return None

    @property
    def gyroscope(self):
        return self.__read_gyroscope_unsafe() or self.gyroscope

    def __read_gyroscope_unsafe(self):
        try:
            self.gyroscope = self.__lsm9ds1.gyroscope
            return self.gyroscope
        except:
            return None