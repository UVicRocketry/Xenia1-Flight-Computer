from adafruit_bme280 import basic as adafruit_bme280


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

    __bme280 = None

    __temperature = None
    __humidity = None
    __pressure = None
    __altitude = None


    def __init__(self, i2c):
        try:
            self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
            self.__bme280.sea_level_pressure = SEA_LEVEL_PRESSURE
        except ValueError:
            self.__bme280 = {
                'pressure': 0,
                'temperature': 0,
                'humidity': 0,
                'altitude': 0
            }

    def refresh(self):
        self.__humidity = self.__read_humidity()
        self.__pressure = self.__read_pressure()
        self.__temperature = self.__read_temperature()
        self.__altitude = self.__read_altitude()


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
        return self.__altitude


    def __read_altitude(self):
        try:
            return self.__bme280.altitude
        except:
            return None
