import adafruit_lsm9ds1
import board


class Lsm:
    """
    lsm sensor object

    ...

    Attributes
    ----------

    __lsm9ds1 : object
        Driver for the lsm sensor, holds methods to
        get each sensor value

    __temperature : float
        Temperature reading from the lsm


    __acceleration : (tuple)
        three axis (x, y, z) of acceleration
        reading from the lsm

    __gyroscope : tuple
        three axis (x, y, z) of gyroscope
        reading from the lsm

    __magnetometer : tuple
        three axis (x, y, z) of magnetometer
        reading from the lsm

    Methods
    -------

    refresh(): reads new values from all sensors on chip and stores the data.

    @property getters: Returns the latest value stored in the variable.

    __read_/.../: Reads the sensor and returns sensor value or None if read was unsuccessful

    """

    __lsm9ds1 = None

    __temperature = None
    __acceleration = None
    __magnetometer = None
    __gyroscope = None

    def __init__(self, i2c):

        try:
            self.__lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        except ValueError:
            self.__lsm9ds1 = {
                'temperature': 0,
                'acceleration': 0,
                'magnetometer': 0,
                'gyroscope': 0
            }

    def refresh(self):
        self.__temperature = self.__read_temperature()
        self.__acceleration = self.__read_acceleration()
        self.__magnetometer = self.__read_magnetometer()
        self.__gyroscope = self.__read_gyroscope()


    @property
    def temperature(self):
        return self.__temperature

    def __read_temperature(self):
        try:
            return self.__lsm9ds1.temperature
        except:
            return None

    @property
    def acceleration(self):
        return self.__acceleration


    def __read_acceleration(self):
        try:
            return self.__lsm9ds1.acceleration
        except:
            return None

    @property
    def magnetometer(self):
        return self.__magnetometer

    def __read_magnetometer(self):
        try:
            return self.__lsm9ds1.magnetometer
        except:
            return None

    @property
    def gyroscope(self):
        return self.__gyroscope


    def __read_gyroscope(self):
        try:
            return self.__lsm9ds1.gyroscope
        except:
            return None