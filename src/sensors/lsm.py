import adafruit_lsm9ds1
import board

class Lsm:
    """
    bme sensor object

    ...

    Attributes
    ----------

    __lsm9ds1 : object
        Driver for lsm sensor, holds methods to
        get each sensor value

    temperature : float
        Temperature reading from lsm

    acceleration : tuple
        three axis (x, y, z) of acceleration
        reading from the lsm

    gyroscope : tuple
        three axis (x, y, z) of gyroscope
        reading from the lsm

    magnetometer : tuple
        three axis (x, y, z) of magnetometer
        reading from the lsm

    Methods
    -------

    read_unsafe_x() : float or None
        Tries to return a sensor value reading
        if the value doesn't read returns None

    """
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

    def read_unsafe_temperature(self):
        try:
            self.temperature = self.__lsm9ds1.temperature
            return self.temperature
        except:
            return None

    def acceleration(self):
        return self.read_acceleration_unsafe() or self.acceleration

    def read_unsafe_acceleration(self):
        try:
            self.acceleration = self.__lsm9ds1.acceleration
            return self.acceleration
        except:
            return None

    @property
    def magnetometer(self):
        return self.read_unsafe_magnetometer() or self.magnetometer

    def read_unsafe_magnetometer(self):
        try:
            self.magnetometer = self.__lsm9ds1.magnetometer
            return self.magnetometer
        except:
            return None

    @property
    def gyroscope(self):
        return self.read_unsafe_gyroscope() or self.gyroscope

    def read_unsafe_gyroscope(self):
        try:
            self.gyroscope = self.__lsm9ds1.gyroscope
            return self.gyroscope
        except:
            return None
