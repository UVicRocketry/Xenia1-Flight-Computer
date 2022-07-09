import adafruit_lsm9ds1
import board
from safe_value import SafeValue



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

    acceleration : SafeValue (tuple)
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

    refresh(): reads new values from all sensors on chip and stores the data. If the data is not critical to calculations it is stored in
    a variable. If it is critical it is stored in a SafeValue object. The variables are named after what is measured. for example,
    __acceleration stores the acceleration SafeValue object.

    @property getters: Returns the latest value stored in the variable or the SafeValue Object. If the specific value is flight critical
    (for example acceleration) there is getters for acceleration which returns non-null values regardless of if sensor is functioning
    and acceleration_unsafe which returns exactly what the sensor read.

    __read_/.../_unsafe(): Reads the sensor and returns sensor value or None if read was unsuccessful

    """
    __lsm9ds1 = None
    
    __temperature = None
    __acceleration = SafeValue([-100,100], 15)
    __magnetometer = None
    __gyroscope = None

    def __init__(self):
        i2c = board.I2C()
        self.__lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
        # TODO: initialize pins (from wiring diagram)

    def refresh(self):
        self.__temperature = self.__read_temperature_unsafe()
        self.__acceleration.update(self.__read_acceleration_unsafe())
        self.__magnetometer = self.__read_magnetometer_unsafe()
        self.__gyroscope = self.__read_gyroscope_unsafe()

    @property
    def temperature(self):
        return self.__temperature

    def __read_temperature_unsafe(self):
        try:
            return self.__lsm9ds1.Temperature
        except:
            return None

    @property
    def acceleration(self):
        return self.__acceleration.get_last_safe_value()

    @property
    def acceleration_unsafe(self):
        return self.__acceleration.get_last_unsafe_value()

    def read_acceleration_unsafe(self):
        try:
            return self.__lsm9ds1.Acceleration
        except:
            return None

    @property
    def magnetometer(self):
        return self.__magnetometer

    def read_magnetometer_unsafe(self):
        try:
            return self.__lsm9ds1.Magnetometer
        except:
            return None

    @property
    def gyroscope(self):
        return self.__gyroscope


    def read_gyroscope_unsafe(self):
        try:
            return self.__lsm9ds1.Gyroscope
        except:
            return None
